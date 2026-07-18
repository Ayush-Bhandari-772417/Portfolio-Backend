from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
import json
import os

from seo.choices import EventType
from seo.models import (
    KeywordRanking, AEOHit, GSCQueryData, GSCCoverage,
    GSCCrawlStats, LocalCitation, SchemaMarkup, Backlink,
    ConversionGoal, ConversionEvent, AICrawlerVisit,
)
from seo.serializers import (
    PublicSEODashboardSerializer,
    ConversionEventSerializer,
    GSCQueryDataSerializer,
    KeywordRankingSerializer,
    BacklinkSerializer,
    LocalCitationSerializer,
)


class SEOStatsAnonThrottle(AnonRateThrottle):
    rate = '30/minute'


class ConversionEventAnonThrottle(AnonRateThrottle):
    rate = '100/minute'


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def dashboard_stats(request):
    """
    Public endpoint for SEO dashboard data.
    Returns aggregated stats from all SEO models.
    """
    last_30 = timezone.now().date() - timedelta(days=30)

    # Keyword rankings
    keyword_qs = KeywordRanking.objects.filter(date__gte=last_30)
    keyword_count = keyword_qs.values('keyword').distinct().count()
    avg_pos = keyword_qs.aggregate(avg=Avg('position'))['avg'] or 0

    # GSC data
    gsc_qs = GSCQueryData.objects.filter(date__gte=last_30)
    total_clicks = gsc_qs.aggregate(total=Sum('clicks'))['total'] or 0
    total_impressions = gsc_qs.aggregate(total=Sum('impressions'))['total'] or 0
    avg_ctr = gsc_qs.aggregate(avg=Avg('ctr'))['avg'] or 0

    # Coverage
    indexed = GSCCoverage.objects.filter(status='indexed').count()

    # Backlinks
    backlink_qs = Backlink.objects.all()
    total_backlinks = backlink_qs.count()
    dofollow = backlink_qs.filter(is_dofollow=True).count()

    # AEO hits
    aeo_qs = AEOHit.objects.filter(date__gte=last_30)
    aeo_total = aeo_qs.count()
    aeo_present = aeo_qs.filter(is_present=True).count()

    # Schema markup
    schema_total = SchemaMarkup.objects.count()
    schema_valid = SchemaMarkup.objects.filter(is_valid=True).count()

    serializer = PublicSEODashboardSerializer({
        'keyword_count': keyword_count,
        'avg_position': round(float(avg_pos), 2),
        'total_clicks_30d': total_clicks,
        'total_impressions_30d': total_impressions,
        'avg_ctr': round(float(avg_ctr), 2),
        'indexed_pages': indexed,
        'total_backlinks': total_backlinks,
        'dofollow_backlinks': dofollow,
        'aeo_features_present': aeo_present,
        'aeo_features_total': aeo_total,
        'schema_valid_count': schema_valid,
        'schema_total_count': schema_total,
    })

    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def keyword_rankings(request):
    """Public read-only keyword rankings"""
    keyword = request.query_params.get('keyword', '')
    days = int(request.query_params.get('days', 30))
    date_from = timezone.now().date() - timedelta(days=days)

    qs = KeywordRanking.objects.filter(
        date__gte=date_from
    ).order_by('-date')

    if keyword:
        qs = qs.filter(keyword__icontains=keyword)

    serializer = KeywordRankingSerializer(qs[:50], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def gsc_queries(request):
    """Public read-only GSC query data"""
    q = request.query_params.get('q', '')
    days = int(request.query_params.get('days', 30))
    date_from = timezone.now().date() - timedelta(days=days)

    qs = GSCQueryData.objects.filter(date__gte=date_from).order_by('-clicks')

    if q:
        qs = qs.filter(query__icontains=q)

    serializer = GSCQueryDataSerializer(qs[:50], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def aeo_features(request):
    """Public read-only AEO features data"""
    days = int(request.query_params.get('days', 30))
    date_from = timezone.now().date() - timedelta(days=days)

    qs = AEOHit.objects.filter(date__gte=date_from).order_by('-date')
    serp_feature = request.query_params.get('feature', '')

    if serp_feature:
        qs = qs.filter(serp_feature=serp_feature)

    data = {
        'total': qs.count(),
        'present': qs.filter(is_present=True).count(),
        'by_feature': list(
            qs.values('serp_feature').annotate(
                total=Count('id'),
                present=Count('id', filter=Q(is_present=True))
            ).order_by('-present')
        ),
        'recent': [
            {
                'keyword': hit.keyword,
                'serp_feature': hit.get_serp_feature_display(),
                'is_present': hit.is_present,
                'position': hit.position,
                'date': hit.date,
            }
            for hit in qs[:20]
        ]
    }

    return Response(data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def backlinks(request):
    """Public read-only backlinks"""
    target = request.query_params.get('target', '')
    qs = Backlink.objects.filter(is_active=True).order_by('-domain_authority')

    if target:
        qs = qs.filter(target_url__icontains=target)

    serializer = BacklinkSerializer(qs[:50], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def crawl_stats(request):
    """Public read-only crawl stats"""
    days = int(request.query_params.get('days', 30))
    date_from = timezone.now().date() - timedelta(days=days)

    qs = GSCCrawlStats.objects.filter(date__gte=date_from).order_by('-date')

    data = {
        'stats': list(qs.values())[:30],
        'totals': {
            'pages_crawled': qs.aggregate(total=Sum('pages_crawled'))['total'] or 0,
            'response_2xx': qs.aggregate(total=Sum('response_2xx'))['total'] or 0,
            'response_4xx': qs.aggregate(total=Sum('response_4xx'))['total'] or 0,
            'response_5xx': qs.aggregate(total=Sum('response_5xx'))['total'] or 0,
        }
    }

    return Response(data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def local_citations(request):
    """Public read-only local citations"""
    qs = LocalCitation.objects.order_by('-last_checked')

    data = {
        'total': qs.count(),
        'consistent': qs.filter(is_consistent=True).count(),
        'inconsistent': qs.filter(is_consistent=False).count(),
        'platforms': list(
            qs.values('platform').annotate(count=Count('id')).order_by('-count')
        ),
        'citations': [
            {
                'platform': c.get_platform_display(),
                'business_name': c.business_name,
                'website': c.website,
                'is_consistent': c.is_consistent,
                'last_checked': c.last_checked,
            }
            for c in qs[:20]
        ]
    }

    return Response(data)


@api_view(['GET'])
@throttle_classes([SEOStatsAnonThrottle])
@permission_classes([AllowAny])
def schema_list(request):
    """Public read-only schema markup list"""
    qs = SchemaMarkup.objects.order_by('page_path')
    schema_type = request.query_params.get('type', '')

    if schema_type:
        qs = qs.filter(schema_type=schema_type)

    data = {
        'total': qs.count(),
        'valid': qs.filter(is_valid=True).count(),
        'invalid': qs.filter(is_valid=False).count(),
        'by_type': list(
            qs.values('schema_type').annotate(count=Count('id')).order_by('-count')
        ),
        'schemas': [
            {
                'page_path': s.page_path,
                'schema_type': s.schema_type,
                'is_valid': s.is_valid,
                'generated_at': s.generated_at,
            }
            for s in qs[:50]
        ]
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def active_goals(request):
    """
    Returns active CRO goals for frontend tracking configuration.
    No throttle needed - this is needed on every page load.
    """
    goals = ConversionGoal.objects.filter(is_active=True).values(
        'id', 'name', 'goal_type', 'target_selector',
        'target_url', 'target_value'
    )
    return Response(list(goals))


@api_view(["POST"])
@throttle_classes([ConversionEventAnonThrottle])
@permission_classes([AllowAny])
def track_event(request):
    """
    Receives analytics/CRO events from the frontend.

    Expected payload:
    {
        "goal_id": 1,                       # optional
        "event_type": "click",             # required
        "event_name": "hire_me_button",    # optional
        "numeric_value": 90,               # optional
        "session_id": "abc123",            # required
        "path": "/projects/my-project",    # required
        "referrer": "https://google.com/", # optional
        "metadata": {},                    # optional
        "user_agent": "Mozilla/5.0..."     # optional
    }
    """

    goal_id = request.data.get("goal_id")
    event_type = request.data.get("event_type")
    event_name = request.data.get("event_name", "")
    numeric_value = request.data.get("numeric_value")
    session_id = request.data.get("session_id")
    path = request.data.get("path")
    referrer = request.data.get("referrer", "")
    metadata = request.data.get("metadata", {})
    user_agent = request.data.get("user_agent", "")

    # ------------------------
    # Required field validation
    # ------------------------

    if not session_id:
        return Response(
            {"error": "session_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not event_type:
        return Response(
            {"error": "event_type is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not path:
        return Response(
            {"error": "path is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------
    # Validate event_type
    # ------------------------

    valid_event_types = {choice[0] for choice in EventType.choices}

    if event_type not in valid_event_types:
        return Response(
            {
                "error": "Invalid event_type.",
                "allowed": list(valid_event_types),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------
    # Optional Goal lookup
    # ------------------------

    goal = None
    if goal_id:
        try:
            goal = ConversionGoal.objects.get(
                pk=goal_id,
                is_active=True,
            )
        except ConversionGoal.DoesNotExist:
            return Response(
                {"error": "Invalid goal_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # ------------------------
    # Create event
    # ------------------------

    event = ConversionEvent.objects.create(
        goal=goal,
        event_type=event_type,
        event_name=event_name,
        numeric_value=numeric_value,
        session_id=session_id,
        path=path,
        referrer=referrer,
        metadata=metadata,
        user_agent=user_agent,
        ip_address=get_client_ip(request),

        # Replace this later with real bot detection.
        is_bot=False,
    )

    serializer = ConversionEventSerializer(event)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )


def get_client_ip(request):
    """Extract client IP from request headers"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(["POST"])
def log_ai_crawler(request):
    """
    Receives AI crawler visits detected by the Next.js middleware.

    This endpoint is intended only for the official frontend.
    """

    allowed_hosts = {
        "www.bhandariayush.com.np",
        "bhandariayush.com.np",
        "localhost",
        "127.0.0.1",
    }

    origin = request.META.get("HTTP_ORIGIN", "")
    referer = request.META.get("HTTP_REFERER", "")

    origin_allowed = any(host in origin for host in allowed_hosts)
    referer_allowed = any(host in referer for host in allowed_hosts)

    # Reject requests from unexpected origins.
    # Requests without Origin/Referer (e.g. server-to-server) are still allowed.
    if (origin or referer) and not (origin_allowed or referer_allowed):
        return Response(
            {"detail": "Forbidden"},
            status=status.HTTP_403_FORBIDDEN,
        )

    valid_crawlers = {
        choice[0]
        for choice in AICrawlerVisit.AI_CRAWLERS
    }

    crawler = request.data.get("crawler", "other_ai")

    if crawler not in valid_crawlers:
        crawler = "other_ai"

    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    AICrawlerVisit.objects.create(
        crawler=crawler,
        user_agent_raw=request.data.get("user_agent", "")[:500],
        path=request.data.get("path", "")[:500],
        host=request.data.get("host", "")[:255],
        canonical=bool(request.data.get("canonical", True)),
        redirected=bool(request.data.get("redirected", False)),
        redirect_reason=request.data.get("redirect_reason") or None,
        ip_address=ip,
    )

    return Response(
        {"status": "logged"},
        status=status.HTTP_201_CREATED,
    )