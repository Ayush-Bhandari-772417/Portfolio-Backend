from django.urls import path, include
from rest_framework.routers import DefaultRouter

from seo.admin.views import (
    KeywordRankingViewSet, AEOHitViewSet, GSCQueryDataViewSet,
    GSCCoverageViewSet, GSCCrawlStatsViewSet, LocalCitationViewSet,
    SchemaMarkupViewSet, BacklinkViewSet, ConversionGoalViewSet,
    ConversionEventViewSet,
)
from seo.public import views as public_views

# Admin router
admin_router = DefaultRouter()
admin_router.register('keyword-rankings', KeywordRankingViewSet, basename='admin-keyword-rankings')
admin_router.register('aeo-hits', AEOHitViewSet, basename='admin-aeo-hits')
admin_router.register('gsc-queries', GSCQueryDataViewSet, basename='admin-gsc-queries')
admin_router.register('gsc-coverage', GSCCoverageViewSet, basename='admin-gsc-coverage')
admin_router.register('gsc-crawl-stats', GSCCrawlStatsViewSet, basename='admin-gsc-crawl-stats')
admin_router.register('local-citations', LocalCitationViewSet, basename='admin-local-citations')
admin_router.register('schema-markup', SchemaMarkupViewSet, basename='admin-schema-markup')
admin_router.register('backlinks', BacklinkViewSet, basename='admin-backlinks')
admin_router.register('conversion-goals', ConversionGoalViewSet, basename='admin-conversion-goals')
admin_router.register('conversion-events', ConversionEventViewSet, basename='admin-conversion-events')

urlpatterns = [
    # Admin endpoints (JWT protected via default permission classes)
    path('admin/', include(admin_router.urls)),

    # Public endpoints (read-only, throttled)
    path('public/dashboard/', public_views.dashboard_stats, name='seo-public-dashboard'),
    path('public/keywords/', public_views.keyword_rankings, name='seo-public-keywords'),
    path('public/gsc-queries/', public_views.gsc_queries, name='seo-public-gsc-queries'),
    path('public/aeo-features/', public_views.aeo_features, name='seo-public-aeo-features'),
    path('public/backlinks/', public_views.backlinks, name='seo-public-backlinks'),
    path('public/crawl-stats/', public_views.crawl_stats, name='seo-public-crawl-stats'),
    path('public/local-citations/', public_views.local_citations, name='seo-public-local-citations'),
    path('public/schemas/', public_views.schema_list, name='seo-public-schemas'),
    path('public/goals/', public_views.active_goals, name='seo-public-goals'),
    path('public/track/', public_views.track_event, name='seo-public-track'),
]

