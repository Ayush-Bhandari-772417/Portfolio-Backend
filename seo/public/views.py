from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
import json

from seo.models import (
    KeywordRanking, AEOHit, GSCQueryData, GSCCoverage,
    GSCCrawlStats, LocalCitation, SchemaMarkup, Backlink,
    ConversionGoal, ConversionEvent,
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


@api_view(['POST'])
@throttle_classes([ConversionEventAnonThrottle])
def track_event(request):
    """
    Receives CRO events from frontend.
    Expected payload:
    {
        "goal_id": 1,
        "session_id": "abc123",
        "url": "https://...",
        "referrer": "https://...",
        "value": 0.0,
        "metadata": {},
        "user_agent": "...",
    }
    """
    goal_id = request.data.get('goal_id')
    session_id = request.data.get('session_id')

    if not goal_id or not session_id:
        return Response(
            {'error': 'goal_id and session_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        goal = ConversionGoal.objects.get(pk=goal_id, is_active=True)
    except ConversionGoal.DoesNotExist:
        return Response(
            {'error': 'Goal not found or inactive'},
            status=status.HTTP_404_NOT_FOUND
        )

    event = ConversionEvent.objects.create(
        goal=goal,
        session_id=session_id,
        url=request.data.get('url', ''),
        referrer=request.data.get('referrer', ''),
        value=request.data.get('value'),
        metadata=request.data.get('metadata', {}),
        user_agent=request.data.get('user_agent', ''),
        ip_address=get_client_ip(request),
    )

    serializer = ConversionEventSerializer(event)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_client_ip(request):
    """Extract client IP from request headers"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

