from django.urls import path, include
from seo.public.ingest_schema import ingest_schema_node
from seo.public.sync import sync_provider
from rest_framework.routers import DefaultRouter

from seo.admin.views import (
    KeywordRankingViewSet, AEOHitViewSet, GSCQueryDataViewSet,
    GSCCoverageViewSet, GSCCrawlStatsViewSet, LocalCitationViewSet,
    SchemaMarkupViewSet, BacklinkViewSet, ConversionGoalViewSet,
    ConversionEventViewSet, AICrawlerVisitViewSet,
)
from seo.public import views as public_views

# Admin router
admin_router = DefaultRouter()
admin_router.register(r'keyword-rankings', KeywordRankingViewSet, basename='admin-keyword-rankings')
admin_router.register(r'aeo-hits', AEOHitViewSet, basename='admin-aeo-hits')
admin_router.register(r'gsc-queries', GSCQueryDataViewSet, basename='admin-gsc-queries')
admin_router.register(r'gsc-coverage', GSCCoverageViewSet, basename='admin-gsc-coverage')
admin_router.register(r'gsc-crawl-stats', GSCCrawlStatsViewSet, basename='admin-gsc-crawl-stats')
admin_router.register(r'local-citations', LocalCitationViewSet, basename='admin-local-citations')
admin_router.register(r'schema-markup', SchemaMarkupViewSet, basename='admin-schema-markup')
admin_router.register(r'backlinks', BacklinkViewSet, basename='admin-backlinks')
admin_router.register(r'conversion-goals', ConversionGoalViewSet, basename='admin-conversion-goals')
admin_router.register(r'conversion-events', ConversionEventViewSet, basename='admin-conversion-events')
admin_router.register(r'ai-crawler-visits', AICrawlerVisitViewSet, basename='admin-ai-crawler-visits')

urlpatterns = [
    # Admin endpoints (JWT protected via default permission classes)
    path('admin/', include(admin_router.urls)),
    
    # Provider sync endpoints (trigger backend management commands)
    # Used by admin frontend: POST /api/seo/sync/<type>/
    path('admin/sync/<str:type>/', sync_provider, name='seo-sync-provider'),

    # Public endpoints (read-only, throttled)
    # Standardized: /api/public/seo/<...>/
    path('public/seo/dashboard/', public_views.dashboard_stats, name='seo-public-dashboard'),
    path('public/seo/keywords/', public_views.keyword_rankings, name='seo-public-keywords'),
    path('public/seo/gsc-queries/', public_views.gsc_queries, name='seo-public-gsc-queries'),
    path('public/seo/aeo-features/', public_views.aeo_features, name='seo-public-aeo-features'),
    path('public/seo/backlinks/', public_views.backlinks, name='seo-public-backlinks'),
    path('public/seo/crawl-stats/', public_views.crawl_stats, name='seo-public-crawl-stats'),
    path('public/seo/local-citations/', public_views.local_citations, name='seo-public-local-citations'),
    path('public/seo/schemas/', public_views.schema_list, name='seo-public-schemas'),
    path('public/seo/goals/', public_views.active_goals, name='seo-public-goals'),
    path('public/seo/track/', public_views.track_event, name='seo-public-track'),
    path('public/seo/log-ai-crawler/', public_views.log_ai_crawler, name='seo-public-log-ai-crawler'),

    # Frontend ingestion endpoint: write SchemaMarkup from JSON-LD nodes
    # path('public/seo/schemas/ingest-node/', 'seo.public.ingest_schema.ingest_schema_node', name='seo-public-schemas-ingest-node'),
    path('public/seo/schemas/ingest-node/', ingest_schema_node, name='seo-public-schemas-ingest-node'),

]