from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from seo.models import (
    KeywordRanking, AEOHit, GSCQueryData, GSCCoverage,
    GSCCrawlStats, LocalCitation, SchemaMarkup, Backlink,
    ConversionGoal, ConversionEvent,
)


@admin.register(KeywordRanking)
class KeywordRankingAdmin(ImportExportModelAdmin):
    list_display = ('keyword', 'position', 'previous_position', 'search_engine', 'device', 'date', 'created_at')
    list_filter = ('search_engine', 'device', 'date')
    search_fields = ('keyword', 'url')
    ordering = ('-date', 'keyword')
    date_hierarchy = 'date'


@admin.register(AEOHit)
class AEOHitAdmin(ImportExportModelAdmin):
    list_display = ('keyword', 'serp_feature', 'is_present', 'position', 'url', 'date', 'created_at')
    list_filter = ('serp_feature', 'is_present', 'date')
    search_fields = ('keyword', 'url', 'feature_text')
    ordering = ('-date', 'keyword')
    date_hierarchy = 'date'


@admin.register(GSCQueryData)
class GSCQueryDataAdmin(ImportExportModelAdmin):
    list_display = ('query', 'page', 'clicks', 'impressions', 'ctr', 'position', 'country', 'device', 'date')
    list_filter = ('country', 'device', 'date')
    search_fields = ('query', 'page')
    ordering = ('-date', '-clicks')
    date_hierarchy = 'date'


@admin.register(GSCCoverage)
class GSCCoverageAdmin(ImportExportModelAdmin):
    list_display = ('url', 'status', 'issue_type', 'last_crawled', 'updated_at')
    list_filter = ('status', 'issue_type', 'updated_at')
    search_fields = ('url',)
    ordering = ('-updated_at',)


@admin.register(GSCCrawlStats)
class GSCCrawlStatsAdmin(ImportExportModelAdmin):
    list_display = ('date', 'pages_crawled', 'response_2xx', 'response_4xx', 'response_5xx', 'created_at')
    ordering = ('-date',)
    date_hierarchy = 'date'


@admin.register(LocalCitation)
class LocalCitationAdmin(ImportExportModelAdmin):
    list_display = ('platform', 'business_name', 'phone', 'website', 'is_consistent', 'last_checked')
    list_filter = ('platform', 'is_consistent')
    search_fields = ('business_name', 'website')
    ordering = ('-last_checked',)


@admin.register(SchemaMarkup)
class SchemaMarkupAdmin(ImportExportModelAdmin):
    list_display = ('page_path', 'schema_type', 'is_valid', 'generated_at', 'created_at')
    list_filter = ('schema_type', 'is_valid', 'generated_at')
    search_fields = ('page_path',)
    ordering = ('page_path', 'schema_type')


@admin.register(Backlink)
class BacklinkAdmin(ImportExportModelAdmin):
    list_display = ('source_url', 'target_url', 'anchor_text', 'domain_authority', 'is_dofollow', 'is_active', 'last_checked')
    list_filter = ('is_dofollow', 'is_active', 'link_type')
    search_fields = ('source_url', 'target_url', 'anchor_text')
    ordering = ('-domain_authority', '-first_seen')


@admin.register(ConversionGoal)
class ConversionGoalAdmin(ImportExportModelAdmin):
    list_display = ('name', 'goal_type', 'target_selector', 'target_url', 'is_active', 'created_at')
    list_filter = ('goal_type', 'is_active')
    search_fields = ('name', 'target_selector', 'target_url')
    ordering = ('name',)


@admin.register(ConversionEvent)
class ConversionEventAdmin(ImportExportModelAdmin):
    list_display = ('goal', 'session_id', 'url', 'value', 'timestamp')
    list_filter = ('goal', 'timestamp')
    search_fields = ('session_id', 'url', 'referrer')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

