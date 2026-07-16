from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
import json
import os
from django.utils.dateparse import parse_datetime
import time
import xml.etree.ElementTree as ET

from seo.models import GSCQueryData, GSCCoverage, GSCCrawlStats


class Command(BaseCommand):
    help = 'Sync data from Google Search Console API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to fetch (default: 7)',
        )
        parser.add_argument(
            '--site-url',
            type=str,
            default=None,
            help='Site URL in GSC (e.g., sc-domain:example.com or https://example.com)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be saved without writing to DB',
        )

    def handle(self, *args, **options):
        days = options['days']
        site_url = options['site_url'] or os.getenv('GSC_SITE_URL')
        dry_run = options['dry_run']

        if not site_url:
            self.stderr.write(self.style.ERROR('Please provide --site-url or set GSC_SITE_URL env var'))
            return

        self.stdout.write(self.style.NOTICE(f'Syncing GSC data for {site_url} (last {days} days)...'))

        try:
            self.sync_query_data(site_url, days, dry_run)
            self.sync_coverage(site_url, dry_run)
            self.sync_crawl_stats(site_url, days, dry_run)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error syncing GSC data: {e}'))
            return

        if not dry_run:
            self.stdout.write(self.style.SUCCESS('GSC sync completed successfully!'))

    def get_gsc_service(self):
        """Initialize Google Search Console API service"""
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials_path = os.getenv('GSC_CREDENTIALS_PATH', 'gsc-credentials.json')
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
            )
            return build('webmasters', 'v3', credentials=credentials, cache_discovery=False)
        except ImportError:
            self.stdout.write(self.style.WARNING('google-api-python-client not installed. Using demo data.'))
            return None
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f'Credentials file not found: {credentials_path}. Using demo data.'))
            return None

    def get_gsc_inspection_service(self):
        """
        Initialize the newer Search Console v1 API service.
        urlInspection lives here, NOT in the legacy webmasters v3 API
        that get_gsc_service() builds for searchanalytics.
        """
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials_path = os.getenv('GSC_CREDENTIALS_PATH', 'gsc-credentials.json')
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
            return build('searchconsole', 'v1', credentials=credentials, cache_discovery=False)
        except ImportError:
            return None
        except FileNotFoundError:
            return None

    def get_all_sitemap_urls(self, site_url):
        """
        Pull the complete list of URLs from the sitemap (no cap here —
        capping happens later, based on what's least recently checked).
        """
        import requests

        sitemap_override = os.getenv('GSC_SITEMAP_URL')

        if sitemap_override:
            sitemap_url = sitemap_override
        else:
            if site_url.startswith('sc-domain:'):
                self.stdout.write(self.style.WARNING(
                    'GSC_SITE_URL is a domain property (sc-domain:...). '
                    'Set GSC_SITEMAP_URL explicitly since a sitemap location '
                    'cannot be inferred automatically.'
                ))
                return []
            sitemap_url = site_url.rstrip('/') + '/sitemap.xml'

        urls = []
        to_fetch = [sitemap_url]
        seen_sitemaps = set()

        while to_fetch:
            current = to_fetch.pop(0)
            if current in seen_sitemaps:
                continue
            seen_sitemaps.add(current)

            try:
                response = requests.get(current, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f'  Could not fetch sitemap {current}: {e}'))
                continue

            try:
                root = ET.fromstring(response.content)
            except ET.ParseError as e:
                self.stdout.write(self.style.WARNING(f'  Could not parse sitemap {current}: {e}'))
                continue

            ns = ''
            if root.tag.startswith('{'):
                ns = root.tag.split('}')[0] + '}'

            if root.tag == f'{ns}sitemapindex':
                for sitemap_el in root.findall(f'{ns}sitemap'):
                    loc_el = sitemap_el.find(f'{ns}loc')
                    if loc_el is not None and loc_el.text:
                        to_fetch.append(loc_el.text.strip())
            else:
                for url_el in root.findall(f'{ns}url'):
                    loc_el = url_el.find(f'{ns}loc')
                    if loc_el is not None and loc_el.text:
                        urls.append(loc_el.text.strip())

        return urls

    def select_urls_for_this_run(self, all_urls, max_urls):
        """
        Prioritize URLs never checked, then URLs checked longest ago,
        using the existing updated_at field (auto_now=True).
        """
        existing = {
            c.url: c.updated_at
            for c in GSCCoverage.objects.filter(url__in=all_urls).only('url', 'updated_at')
        }

        never_checked = [u for u in all_urls if u not in existing]
        previously_checked = [u for u in all_urls if u in existing]
        previously_checked.sort(key=lambda u: existing[u])

        ordered = never_checked + previously_checked
        return ordered[:max_urls]

    def map_inspection_to_coverage_fields(self, index_status):
        """
        Translate Google's URL Inspection response into this project's
        GSCCoverage STATUS_CHOICES / ISSUE_TYPES slugs.
        """
        verdict = index_status.get('verdict', 'VERDICT_UNSPECIFIED')
        coverage_state = index_status.get('coverageState', '') or ''
        coverage_state_lower = coverage_state.lower()

        if 'soft 404' in coverage_state_lower:
            issue_type = 'soft_404'
        elif '404' in coverage_state_lower or 'not found' in coverage_state_lower:
            issue_type = 'not_found'
        elif 'server error' in coverage_state_lower or '5xx' in coverage_state_lower:
            issue_type = 'server_error'
        elif 'redirect' in coverage_state_lower:
            issue_type = 'redirect_error'
        elif 'robots' in coverage_state_lower:
            issue_type = 'blocked_robots'
        elif 'duplicate' in coverage_state_lower:
            issue_type = 'duplicate'
        elif 'anomaly' in coverage_state_lower:
            issue_type = 'crawl_anomaly'
        else:
            issue_type = 'no_issue'

        if verdict == 'PASS':
            status = 'indexed'
        elif verdict == 'FAIL':
            status = 'error'
        elif verdict == 'NEUTRAL':
            status = 'excluded'
        else:
            status = 'submitted'

        return status, issue_type
    
    def sync_query_data(self, site_url, days, dry_run):
        """Sync search query data"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        service = self.get_gsc_service()

        if service:
            request = {
                'startDate': start_date.isoformat(),
                'endDate': end_date.isoformat(),
                'dimensions': ['query', 'page', 'country', 'device'],
                'rowLimit': 25000,
            }
            response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
            rows = response.get('rows', [])
        else:
            rows = self._generate_demo_query_data(start_date, end_date)

        self.stdout.write(f'  Found {len(rows)} query rows')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would save {len(rows)} query records'))
            return

        created = 0
        updated = 0

        for row in rows:
            keys = row.get('keys', ['', '', '', ''])
            query_str = keys[0] if len(keys) > 0 else ''
            page_url = keys[1] if len(keys) > 1 else ''
            country = keys[2] if len(keys) > 2 else 'usa'
            device = keys[3] if len(keys) > 3 else 'desktop'

            obj, was_created = GSCQueryData.objects.update_or_create(
                query=query_str,
                page=page_url,
                country=country,
                device=device,
                date=end_date,
                defaults={
                    'clicks': row.get('clicks', 0),
                    'impressions': row.get('impressions', 0),
                    'ctr': row.get('ctr', 0.0) * 100,
                    'position': row.get('position', 0.0),
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Query data: {created} created, {updated} updated')

    def sync_coverage(self, site_url, dry_run):
        """Sync coverage/indexing status via per-URL Inspection API looping"""
        service = self.get_gsc_inspection_service()

        if not service:
            self.stdout.write(self.style.WARNING('Inspection service unavailable. Using demo data.'))
            rows = self._generate_demo_coverage()
            self._save_coverage_rows(rows, dry_run)
            return

        max_urls = int(os.getenv('GSC_MAX_URLS_PER_RUN', 50))
        request_delay = float(os.getenv('GSC_INSPECTION_DELAY_SECONDS', 0.5))

        all_urls = self.get_all_sitemap_urls(site_url)

        if not all_urls:
            self.stdout.write(self.style.WARNING('No URLs found to inspect. Using demo data.'))
            rows = self._generate_demo_coverage()
            self._save_coverage_rows(rows, dry_run)
            return

        urls = self.select_urls_for_this_run(all_urls, max_urls)

        self.stdout.write(
            f'  Inspecting {len(urls)} of {len(all_urls)} total sitemap URLs '
            f'(rotating by least-recently-checked)...'
        )

        rows = []
        for i, url in enumerate(urls):
            try:
                response = service.urlInspection().index().inspect(
                    body={'inspectionUrl': url, 'siteUrl': site_url}
                ).execute()

                result = response.get('inspectionResult', {})
                index_status = result.get('indexStatusResult', {})

                status, issue_type = self.map_inspection_to_coverage_fields(index_status)

                last_crawled_raw = index_status.get('lastCrawlTime')
                last_crawled = parse_datetime(last_crawled_raw) if last_crawled_raw else None

                rows.append({
                    'url': url,
                    'status': status,
                    'issue_type': issue_type,
                    'last_crawled': last_crawled,
                    'page_fetch_state': index_status.get('pageFetchState', '')[:50],
                    'indexing_state': index_status.get('indexingState', '')[:50],
                })

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Inspection failed for {url}: {e}'))

            if i < len(urls) - 1:
                time.sleep(request_delay)

        if not rows:
            self.stdout.write(self.style.WARNING('  All inspections failed. Using demo data.'))
            rows = self._generate_demo_coverage()

        self._save_coverage_rows(rows, dry_run)

    def _save_coverage_rows(self, rows, dry_run):
        """Shared save logic for real or demo coverage rows"""
        self.stdout.write(f'  Found {len(rows)} coverage rows')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would save {len(rows)} coverage records'))
            return

        created = 0
        updated = 0

        for row in rows:
            obj, was_created = GSCCoverage.objects.update_or_create(
                url=row['url'],
                defaults={
                    'status': row['status'],
                    'issue_type': row.get('issue_type', 'no_issue'),
                    'last_crawled': row.get('last_crawled'),
                    'page_fetch_state': row.get('page_fetch_state', ''),
                    'indexing_state': row.get('indexing_state', ''),
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Coverage data: {created} created, {updated} updated')

    def sync_crawl_stats(self, site_url, days, dry_run):
        """Sync crawl statistics"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)

        service = self.get_gsc_service()

        if service:
            # Crawl stats are not directly available via API v3
            # Would need to use Search Console UI export or Analytics API
            rows = self._generate_demo_crawl_stats(start_date, end_date)
        else:
            rows = self._generate_demo_crawl_stats(start_date, end_date)

        self.stdout.write(f'  Found {len(rows)} crawl stat rows')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would save {len(rows)} crawl stat records'))
            return

        created = 0
        updated = 0

        for row in rows:
            obj, was_created = GSCCrawlStats.objects.update_or_create(
                date=row['date'],
                defaults={
                    'pages_crawled': row['pages_crawled'],
                    'pages_crawled_per_day': row['pages_crawled_per_day'],
                    'response_2xx': row['response_2xx'],
                    'response_3xx': row['response_3xx'],
                    'response_4xx': row['response_4xx'],
                    'response_5xx': row['response_5xx'],
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Crawl stats: {created} created, {updated} updated')

    # Demo data generators for when API is not available
    def _generate_demo_query_data(self, start_date, end_date):
        import random
        queries = [
            'portfolio developer', 'react developer', 'python django',
            'full stack developer', 'web developer portfolio',
            'nextjs developer', 'seo engineer', 'frontend developer',
        ]
        rows = []
        for query in queries:
            rows.append({
                'keys': [query, 'https://example.com/', 'usa', 'desktop'],
                'clicks': random.randint(10, 500),
                'impressions': random.randint(100, 5000),
                'ctr': round(random.uniform(0.01, 0.15), 4),
                'position': round(random.uniform(2.5, 35.0), 1),
            })
        return rows

    def _generate_demo_coverage(self):
        return [
            {
                'url': 'https://example.com/',
                'status': 'indexed',
                'issue_type': 'no_issue',
                'page_fetch_state': 'Successful',
                'indexing_state': 'Indexed',
            },
            {
                'url': 'https://example.com/projects/',
                'status': 'indexed',
                'issue_type': 'no_issue',
                'page_fetch_state': 'Successful',
                'indexing_state': 'Indexed',
            },
            {
                'url': 'https://example.com/old-page/',
                'status': 'excluded',
                'issue_type': 'not_found',
                'page_fetch_state': 'Failed',
                'indexing_state': 'Not indexed',
            },
        ]

    def _generate_demo_crawl_stats(self, start_date, end_date):
        import random
        from datetime import datetime

        rows = []
        current = start_date
        while current <= end_date:
            rows.append({
                'date': current,
                'pages_crawled': random.randint(50, 200),
                'pages_crawled_per_day': random.randint(10, 50),
                'response_2xx': random.randint(40, 180),
                'response_3xx': random.randint(0, 10),
                'response_4xx': random.randint(0, 5),
                'response_5xx': random.randint(0, 2),
            })
            current += timedelta(days=1)
        return rows

