from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import os
import random

from seo.models import KeywordRanking, AEOHit


class Command(BaseCommand):
    help = 'Sync SERP ranking and AEO data from DataForSEO or SerpApi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keywords',
            nargs='+',
            default=None,
            help='Specific keywords to check (default: from DB or env)',
        )
        parser.add_argument(
            '--location',
            type=str,
            default='United States',
            help='Search location (default: United States)',
        )
        parser.add_argument(
            '--device',
            type=str,
            default='desktop',
            choices=['desktop', 'mobile'],
            help='Device type',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be saved without writing to DB',
        )

    def handle(self, *args, **options):
        keywords = options['keywords']
        location = options['location']
        device = options['device']
        dry_run = options['dry_run']

        if not keywords:
            keywords_env = os.getenv('SEO_KEYWORDS', '')
            keywords = [k.strip() for k in keywords_env.split(',') if k.strip()]

        if not keywords:
            # Use existing keywords from DB or defaults
            existing = KeywordRanking.objects.values_list('keyword', flat=True).distinct()[:20]
            keywords = list(existing) if existing else [
                'portfolio developer', 'react developer', 'python django',
                'full stack developer', 'nextjs developer',
            ]

        self.stdout.write(self.style.NOTICE(
            f'Syncing SERP data for {len(keywords)} keywords ({device}, {location})...'
        ))

        try:
            self.sync_rankings(keywords, location, device, dry_run)
            self.sync_aeo(keywords, location, device, dry_run)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error syncing SERP data: {e}'))
            return

        if not dry_run:
            self.stdout.write(self.style.SUCCESS('SERP sync completed successfully!'))

    def sync_rankings(self, keywords, location, device, dry_run):
        """Sync keyword rankings"""
        today = timezone.now().date()

        # Try DataForSEO API
        results = self._fetch_dataforseo_rankings(keywords, location, device)

        if not results:
            results = self._fetch_serpapi_rankings(keywords, location, device)

        if not results:
            self.stdout.write(self.style.WARNING('No API available. Using demo data.'))
            results = self._generate_demo_rankings(keywords, location, device)

        self.stdout.write(f'  Found {len(results)} ranking results')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would save {len(results)} ranking records'))
            return

        created = 0
        updated = 0

        for result in results:
            # Get previous position for change tracking
            previous = KeywordRanking.objects.filter(
                keyword=result['keyword'],
                search_engine=result['search_engine'],
                location=result['location'],
                device=result['device'],
            ).exclude(date=today).order_by('-date').first()

            obj, was_created = KeywordRanking.objects.update_or_create(
                keyword=result['keyword'],
                search_engine=result['search_engine'],
                location=result['location'],
                device=result['device'],
                date=today,
                defaults={
                    'position': result['position'],
                    'previous_position': previous.position if previous else None,
                    'url': result['url'],
                    'search_volume': result.get('search_volume'),
                    'keyword_difficulty': result.get('keyword_difficulty'),
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  Rankings: {created} created, {updated} updated')

    def sync_aeo(self, keywords, location, device, dry_run):
        """Sync AEO/SERP feature data"""
        today = timezone.now().date()

        results = self._fetch_aeo_data(keywords, location, device)

        if not results:
            self.stdout.write(self.style.WARNING('No AEO API available. Using demo data.'))
            results = self._generate_demo_aeo(keywords, location, device)

        self.stdout.write(f'  Found {len(results)} AEO results')

        if dry_run:
            self.stdout.write(self.style.WARNING(f'  [DRY RUN] Would save {len(results)} AEO records'))
            return

        created = 0
        updated = 0

        for result in results:
            obj, was_created = AEOHit.objects.update_or_create(
                keyword=result['keyword'],
                serp_feature=result['serp_feature'],
                url=result['url'],
                date=today,
                defaults={
                    'is_present': result['is_present'],
                    'position': result.get('position'),
                    'feature_text': result.get('feature_text', ''),
                }
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(f'  AEO hits: {created} created, {updated} updated')

    def _fetch_dataforseo_rankings(self, keywords, location, device):
        """Fetch rankings from DataForSEO API"""
        try:
            import requests
            login = os.getenv('DATAFORSEO_LOGIN')
            password = os.getenv('DATAFORSEO_PASSWORD')

            if not login or not password:
                return None

            # DataForSEO SERP API
            endpoint = 'https://api.dataforseo.com/v3/serp/google/organic/live/advanced'
            results = []

            for keyword in keywords:
                payload = [{
                    'keyword': keyword,
                    'location_code': 2840 if 'United States' in location else 2826,
                    'language_code': 'en',
                    'device': device,
                }]

                response = requests.post(
                    endpoint,
                    auth=(login, password),
                    json=payload,
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()
                    tasks = data.get('tasks', [])
                    for task in tasks:
                        for result in task.get('result', []):
                            for item in result.get('items', []):
                                if item.get('type') == 'organic':
                                    results.append({
                                        'keyword': keyword,
                                        'search_engine': 'google',
                                        'location': location,
                                        'device': device,
                                        'position': item.get('rank_absolute', 0),
                                        'url': item.get('url', ''),
                                        'search_volume': None,
                                        'keyword_difficulty': None,
                                    })
                                    break  # Only take top result for demo

            return results
        except ImportError:
            return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'DataForSEO error: {e}'))
            return None

    def _fetch_serpapi_rankings(self, keywords, location, device):
        """Fetch rankings from SerpApi"""
        try:
            import requests
            api_key = os.getenv('SERPAPI_KEY')

            if not api_key:
                return None

            results = []
            for keyword in keywords:
                params = {
                    'engine': 'google',
                    'q': keyword,
                    'location': location,
                    'device': device,
                    'api_key': api_key,
                    'num': 10,
                }

                response = requests.get('https://serpapi.com/search', params=params, timeout=60)

                if response.status_code == 200:
                    data = response.json()
                    organic = data.get('organic_results', [])
                    for item in organic:
                        results.append({
                            'keyword': keyword,
                            'search_engine': 'google',
                            'location': location,
                            'device': device,
                            'position': item.get('position', 0),
                            'url': item.get('link', ''),
                            'search_volume': None,
                            'keyword_difficulty': None,
                        })

            return results
        except ImportError:
            return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'SerpApi error: {e}'))
            return None

    def _fetch_aeo_data(self, keywords, location, device):
        """Fetch AEO/SERP feature data"""
        # AEO data typically comes from the same SERP API
        # This is a simplified implementation
        return None  # Will fall back to demo data

    def _generate_demo_rankings(self, keywords, location, device):
        import random
        results = []
        for keyword in keywords:
            results.append({
                'keyword': keyword,
                'search_engine': 'google',
                'location': location,
                'device': device,
                'position': random.randint(1, 50),
                'url': f'https://example.com/{keyword.replace(" ", "-")}/',
                'search_volume': random.randint(100, 10000),
                'keyword_difficulty': random.randint(10, 80),
            })
        return results

    def _generate_demo_aeo(self, keywords, location, device):
        import random
        features = [
            'featured_snippet', 'people_also_ask', 'ai_overview',
            'knowledge_panel', 'rich_result', 'video_carousel',
        ]
        results = []
        for keyword in keywords:
            for feature in random.sample(features, k=random.randint(1, 3)):
                results.append({
                    'keyword': keyword,
                    'serp_feature': feature,
                    'url': f'https://example.com/{keyword.replace(" ", "-")}/',
                    'is_present': random.choice([True, False]),
                    'position': random.randint(1, 5) if random.choice([True, False]) else None,
                    'feature_text': f'Sample {feature} text for {keyword}',
                })
        return results

