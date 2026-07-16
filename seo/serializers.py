from rest_framework import serializers
from seo.models import (
    KeywordRanking, AEOHit, GSCQueryData, GSCCoverage,
    GSCCrawlStats, LocalCitation, SchemaMarkup, Backlink,
    ConversionGoal, ConversionEvent, AICrawlerVisit
)


class KeywordRankingSerializer(serializers.ModelSerializer):
    position_change = serializers.IntegerField(read_only=True)

    class Meta:
        model = KeywordRanking
        fields = '__all__'


class KeywordRankingStatsSerializer(serializers.Serializer):
    """Aggregated stats for dashboard"""
    total_keywords = serializers.IntegerField()
    keywords_in_top_3 = serializers.IntegerField()
    keywords_in_top_10 = serializers.IntegerField()
    avg_position = serializers.FloatField()
    position_improved = serializers.IntegerField()
    position_dropped = serializers.IntegerField()


class AEOHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AEOHit
        fields = '__all__'


class AEOHitStatsSerializer(serializers.Serializer):
    """Aggregated AEO stats"""
    total_features = serializers.IntegerField()
    present_count = serializers.IntegerField()
    missing_count = serializers.IntegerField()
    by_feature = serializers.DictField()


class GSCQueryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSCQueryData
        fields = '__all__'


class GSCCoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSCCoverage
        fields = '__all__'


class GSCCoverageStatsSerializer(serializers.Serializer):
    total_pages = serializers.IntegerField()
    indexed = serializers.IntegerField()
    excluded = serializers.IntegerField()
    errors = serializers.IntegerField()
    warnings = serializers.IntegerField()


class GSCCrawlStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSCCrawlStats
        fields = '__all__'


class LocalCitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalCitation
        fields = '__all__'


class SchemaMarkupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaMarkup
        fields = '__all__'


class BacklinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backlink
        fields = '__all__'


class BacklinkStatsSerializer(serializers.Serializer):
    total_backlinks = serializers.IntegerField()
    dofollow_count = serializers.IntegerField()
    nofollow_count = serializers.IntegerField()
    avg_domain_authority = serializers.FloatField()
    active_links = serializers.IntegerField()
    broken_links = serializers.IntegerField()


class ConversionGoalSerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(read_only=True, source='events.count')

    class Meta:
        model = ConversionGoal
        fields = '__all__'


class ConversionGoalCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionGoal
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ConversionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionEvent
        fields = '__all__'
        read_only_fields = ('timestamp',)


class AICrawlerVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICrawlerVisit
        fields = '__all__'
        read_only_fields = ('timestamp',)


class PublicSEODashboardSerializer(serializers.Serializer):
    """Combined public-facing SEO stats"""
    keyword_count = serializers.IntegerField()
    avg_position = serializers.FloatField()
    total_clicks_30d = serializers.IntegerField()
    total_impressions_30d = serializers.IntegerField()
    avg_ctr = serializers.FloatField()
    indexed_pages = serializers.IntegerField()
    total_backlinks = serializers.IntegerField()
    dofollow_backlinks = serializers.IntegerField()
    aeo_features_present = serializers.IntegerField()
    aeo_features_total = serializers.IntegerField()
    schema_valid_count = serializers.IntegerField()
    schema_total_count = serializers.IntegerField()

