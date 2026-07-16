from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg, Q, F, Sum
from django.utils import timezone
from datetime import timedelta

from seo.models import (
    KeywordRanking, AEOHit, GSCQueryData, GSCCoverage,
    GSCCrawlStats, LocalCitation, SchemaMarkup, Backlink,
    ConversionGoal, ConversionEvent, AICrawlerVisit,
)
from seo.serializers import (
    KeywordRankingSerializer, KeywordRankingStatsSerializer,
    AEOHitSerializer, AEOHitStatsSerializer,
    GSCQueryDataSerializer, GSCCoverageSerializer,
    GSCCoverageStatsSerializer, GSCCrawlStatsSerializer,
    LocalCitationSerializer, SchemaMarkupSerializer,
    BacklinkSerializer, BacklinkStatsSerializer,
    ConversionGoalSerializer, ConversionGoalCreateUpdateSerializer,
    ConversionEventSerializer, AICrawlerVisitSerializer,
)


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class KeywordRankingViewSet(viewsets.ModelViewSet):
    """Admin CRUD for keyword rankings"""
    queryset = KeywordRanking.objects.all()
    serializer_class = KeywordRankingSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        if keyword:
            qs = qs.filter(keyword__icontains=keyword)
        return qs

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Aggregated keyword stats"""
        last_30 = timezone.now().date() - timedelta(days=30)
        qs = self.get_queryset().filter(date__gte=last_30)

        total = qs.values('keyword').distinct().count()
        top_3 = qs.filter(position__lte=3).values('keyword').distinct().count()
        top_10 = qs.filter(position__lte=10).values('keyword').distinct().count()
        avg_pos = qs.aggregate(avg=Avg('position'))['avg'] or 0

        improved = qs.filter(
            previous_position__isnull=False,
            position__lt=F('previous_position')
        ).count()
        dropped = qs.filter(
            previous_position__isnull=False,
            position__gt=F('previous_position')
        ).count()

        serializer = KeywordRankingStatsSerializer({
            'total_keywords': total,
            'keywords_in_top_3': top_3,
            'keywords_in_top_10': top_10,
            'avg_position': round(float(avg_pos), 2),
            'position_improved': improved,
            'position_dropped': dropped,
        })
        return Response(serializer.data)


class AEOHitViewSet(viewsets.ModelViewSet):
    """Admin CRUD for AEO hits"""
    queryset = AEOHit.objects.all()
    serializer_class = AEOHitSerializer
    pagination_class = StandardPagination

    @action(detail=False, methods=['get'])
    def stats(self, request):
        last_30 = timezone.now().date() - timedelta(days=30)
        qs = self.get_queryset().filter(date__gte=last_30)

        total = qs.count()
        present = qs.filter(is_present=True).count()
        missing = total - present

        by_feature = qs.filter(is_present=True).values('serp_feature').annotate(
            count=Count('id')
        ).order_by('-count')

        serializer = AEOHitStatsSerializer({
            'total_features': total,
            'present_count': present,
            'missing_count': missing,
            'by_feature': {item['serp_feature']: item['count'] for item in by_feature},
        })
        return Response(serializer.data)


class GSCQueryDataViewSet(viewsets.ModelViewSet):
    """Admin CRUD for GSC query data"""
    queryset = GSCQueryData.objects.all()
    serializer_class = GSCQueryDataSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            qs = qs.filter(query__icontains=query)
        return qs


class GSCCoverageViewSet(viewsets.ModelViewSet):
    """Admin CRUD for GSC coverage"""
    queryset = GSCCoverage.objects.all()
    serializer_class = GSCCoverageSerializer
    pagination_class = StandardPagination

    @action(detail=False, methods=['get'])
    def stats(self, request):
        qs = self.get_queryset()
        total = qs.count()
        indexed = qs.filter(status='indexed').count()
        excluded = qs.filter(status='excluded').count()
        errors = qs.filter(status='error').count()
        warnings = qs.filter(status='warning').count()

        serializer = GSCCoverageStatsSerializer({
            'total_pages': total,
            'indexed': indexed,
            'excluded': excluded,
            'errors': errors,
            'warnings': warnings,
        })
        return Response(serializer.data)


class GSCCrawlStatsViewSet(viewsets.ModelViewSet):
    """Admin CRUD for GSC crawl stats"""
    queryset = GSCCrawlStats.objects.all()
    serializer_class = GSCCrawlStatsSerializer
    pagination_class = StandardPagination


class LocalCitationViewSet(viewsets.ModelViewSet):
    """Admin CRUD for local citations"""
    queryset = LocalCitation.objects.all()
    serializer_class = LocalCitationSerializer
    pagination_class = StandardPagination


class SchemaMarkupViewSet(viewsets.ModelViewSet):
    """Admin CRUD for schema markup"""
    queryset = SchemaMarkup.objects.all()
    serializer_class = SchemaMarkupSerializer
    pagination_class = StandardPagination

    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate schema JSON against known types"""
        schema_id = request.data.get('id')
        try:
            schema = self.get_queryset().get(pk=schema_id)
        except SchemaMarkup.DoesNotExist:
            return Response({'error': 'Schema not found'}, status=status.HTTP_404_NOT_FOUND)

        errors = []
        json_content = schema.json_content

        if '@context' not in str(json_content):
            errors.append("Missing @context")
        if '@type' not in str(json_content):
            errors.append("Missing @type")

        schema.is_valid = len(errors) == 0
        schema.validation_errors = errors
        schema.save()

        return Response({
            'is_valid': schema.is_valid,
            'errors': errors,
        })


class BacklinkViewSet(viewsets.ModelViewSet):
    """Admin CRUD for backlinks"""
    queryset = Backlink.objects.all()
    serializer_class = BacklinkSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        target = self.request.query_params.get('target_url')
        if target:
            qs = qs.filter(target_url__icontains=target)
        return qs

    @action(detail=False, methods=['get'])
    def stats(self, request):
        qs = self.get_queryset()
        total = qs.count()
        dofollow = qs.filter(is_dofollow=True).count()
        nofollow = qs.filter(is_dofollow=False).count()
        avg_da = qs.aggregate(avg=Avg('domain_authority'))['avg'] or 0
        active = qs.filter(is_active=True).count()
        broken = qs.filter(is_active=False).count()

        serializer = BacklinkStatsSerializer({
            'total_backlinks': total,
            'dofollow_count': dofollow,
            'nofollow_count': nofollow,
            'avg_domain_authority': round(float(avg_da), 2),
            'active_links': active,
            'broken_links': broken,
        })
        return Response(serializer.data)


class ConversionGoalViewSet(viewsets.ModelViewSet):
    """Admin CRUD for CRO goals"""
    queryset = ConversionGoal.objects.all()
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversionGoalCreateUpdateSerializer
        return ConversionGoalSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """List only active goals (for frontend tracking config)"""
        goals = self.get_queryset().filter(is_active=True)
        serializer = ConversionGoalSerializer(goals, many=True)
        return Response(serializer.data)


class ConversionEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Admin read-only view of CRO events"""
    queryset = ConversionEvent.objects.all()
    serializer_class = ConversionEventSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        goal = self.request.query_params.get('goal')
        if goal:
            qs = qs.filter(goal_id=goal)
        return qs


class AICrawlerVisitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AICrawlerVisitSerializer
    pagination_class = StandardPagination

    queryset = (
        AICrawlerVisit.objects.only(
            "id", "crawler", "host", "path", "canonical", "redirected", "redirect_reason",
            "timestamp", "ip_address", "user_agent_raw",
        ).order_by("-timestamp")
    )

    filterset_fields = ("crawler", "host", "canonical", "redirected",)
    search_fields = ("path","host","user_agent_raw",)
    ordering_fields = ("timestamp", "crawler", "host", "path",)
    ordering = ("-timestamp",)