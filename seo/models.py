from django.db import models
from django.conf import settings


class KeywordRanking(models.Model):
    """SEO Rankings Tracker - populated by SERP API (DataForSEO/SerpApi)"""
    keyword = models.CharField(max_length=255, db_index=True)
    search_engine = models.CharField(max_length=50, default='google', choices=[
        ('google', 'Google'),
        ('bing', 'Bing'),
    ])
    location = models.CharField(max_length=100, default='United States')
    device = models.CharField(max_length=20, default='desktop', choices=[
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
    ])
    position = models.PositiveIntegerField()
    previous_position = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()
    search_volume = models.PositiveIntegerField(null=True, blank=True)
    keyword_difficulty = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'keyword']
        unique_together = [['keyword', 'search_engine', 'location', 'device', 'date']]
        indexes = [
            models.Index(fields=['keyword', '-date']),
            models.Index(fields=['url', '-date']),
        ]

    def __str__(self):
        return f"{self.keyword} - Position {self.position} ({self.date})"

    @property
    def position_change(self):
        if self.previous_position is None:
            return None
        return self.previous_position - self.position


class AEOHit(models.Model):
    """AEO Hit Counter - populated by SERP scraping (DataForSEO/SerpApi)"""
    SERP_FEATURES = [
        ('featured_snippet', 'Featured Snippet'),
        ('people_also_ask', 'People Also Ask'),
        ('ai_overview', 'AI Overview'),
        ('knowledge_panel', 'Knowledge Panel'),
        ('rich_result', 'Rich Result'),
        ('video_carousel', 'Video Carousel'),
        ('image_pack', 'Image Pack'),
        ('top_stories', 'Top Stories'),
    ]

    keyword = models.CharField(max_length=255, db_index=True)
    serp_feature = models.CharField(max_length=30, choices=SERP_FEATURES, db_index=True)
    url = models.URLField()
    is_present = models.BooleanField(default=False)
    position = models.PositiveIntegerField(null=True, blank=True)
    feature_text = models.TextField(blank=True)
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'keyword', 'serp_feature']
        unique_together = [['keyword', 'serp_feature', 'url', 'date']]
        indexes = [
            models.Index(fields=['serp_feature', '-date']),
            models.Index(fields=['is_present', '-date']),
        ]

    def __str__(self):
        status = "Present" if self.is_present else "Missing"
        return f"{self.keyword} - {self.serp_feature} ({status})"


class GSCQueryData(models.Model):
    """Google Search Console Query Data - populated by GSC API"""
    query = models.CharField(max_length=500, db_index=True)
    page = models.URLField(db_index=True)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    ctr = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    position = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    country = models.CharField(max_length=10, default='usa')
    device = models.CharField(max_length=20, default='desktop')
    date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-clicks']
        unique_together = [['query', 'page', 'country', 'device', 'date']]
        indexes = [
            models.Index(fields=['query', '-date']),
            models.Index(fields=['page', '-date']),
        ]

    def __str__(self):
        return f"{self.query} - {self.clicks} clicks ({self.date})"


class GSCCoverage(models.Model):
    """GSC Coverage/Indexing Status - populated by GSC API"""
    STATUS_CHOICES = [
        ('indexed', 'Indexed'),
        ('excluded', 'Excluded'),
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('submitted', 'Submitted'),
    ]
    ISSUE_TYPES = [
        ('no_issue', 'No Issue'),
        ('not_found', 'Not Found (404)'),
        ('server_error', 'Server Error (5xx)'),
        ('redirect_error', 'Redirect Error'),
        ('blocked_robots', 'Blocked by Robots'),
        ('duplicate', 'Duplicate without Canonical'),
        ('soft_404', 'Soft 404'),
        ('crawl_anomaly', 'Crawl Anomaly'),
    ]

    url = models.URLField(unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True)
    issue_type = models.CharField(max_length=30, choices=ISSUE_TYPES, default='no_issue')
    last_crawled = models.DateTimeField(null=True, blank=True)
    last_submitted = models.DateTimeField(null=True, blank=True)
    sitemap = models.URLField(blank=True)
    page_fetch_state = models.CharField(max_length=50, blank=True)
    indexing_state = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status', '-updated_at']),
            models.Index(fields=['issue_type', '-updated_at']),
        ]

    def __str__(self):
        return f"{self.url} - {self.status}"


class GSCCrawlStats(models.Model):
    """GSC Crawl Statistics - populated by GSC API"""
    date = models.DateField(unique=True, db_index=True)
    pages_crawled = models.PositiveIntegerField(default=0)
    pages_crawled_per_day = models.PositiveIntegerField(default=0)
    response_2xx = models.PositiveIntegerField(default=0)
    response_3xx = models.PositiveIntegerField(default=0)
    response_4xx = models.PositiveIntegerField(default=0)
    response_5xx = models.PositiveIntegerField(default=0)
    time_spent_ms = models.PositiveIntegerField(default=0)
    kilobytes_downloaded = models.PositiveIntegerField(default=0)
    host = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Crawl Stats - {self.date}"


class LocalCitation(models.Model):
    """Local SEO NAP Consistency - populated manually or by scraping"""
    PLATFORM_CHOICES = [
        ('google_business', 'Google Business Profile'),
        ('yelp', 'Yelp'),
        ('bing', 'Bing Places'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter/X'),
        ('apple_maps', 'Apple Maps'),
        ('tripadvisor', 'TripAdvisor'),
        ('other', 'Other'),
    ]

    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, db_index=True)
    platform_url = models.URLField(blank=True)
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    is_consistent = models.BooleanField(default=True, db_index=True)
    inconsistencies = models.JSONField(default=dict, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_checked']
        unique_together = [['platform', 'business_name']]

    def __str__(self):
        status = "Consistent" if self.is_consistent else "Inconsistent"
        return f"{self.platform} - {status}"


class SchemaMarkup(models.Model):
    """Advanced Schema Types tracking"""
    SCHEMA_TYPES = [
        ('Organization', 'Organization'),
        ('Person', 'Person'),
        ('HowTo', 'HowTo'),
        ('Course', 'Course'),
        ('Event', 'Event'),
        ('JobPosting', 'Job Posting'),
        ('Product', 'Product'),
        ('Review', 'Review'),
        ('AggregateRating', 'Aggregate Rating'),
        ('FAQPage', 'FAQ Page'),
        ('Article', 'Article'),
        ('BlogPosting', 'Blog Posting'),
        ('WebSite', 'WebSite'),
        ('BreadcrumbList', 'Breadcrumb List'),
        ('SpeakableSpecification', 'Speakable'),
    ]

    page_path = models.CharField(max_length=500, db_index=True)
    schema_type = models.CharField(max_length=30, choices=SCHEMA_TYPES, db_index=True)
    json_content = models.JSONField()
    is_valid = models.BooleanField(default=False, db_index=True)
    validation_errors = models.JSONField(default=list, blank=True)
    generated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['page_path', 'schema_type']
        unique_together = [['page_path', 'schema_type']]
        indexes = [
            models.Index(fields=['schema_type', 'is_valid']),
        ]

    def __str__(self):
        return f"{self.page_path} - {self.schema_type}"


class Backlink(models.Model):
    """Backlink Monitoring - populated by Ahrefs/Moz/Majestic API"""
    source_url = models.URLField(db_index=True)
    target_url = models.URLField(db_index=True)
    anchor_text = models.CharField(max_length=500, blank=True)
    domain_authority = models.PositiveIntegerField(null=True, blank=True)
    page_authority = models.PositiveIntegerField(null=True, blank=True)
    is_dofollow = models.BooleanField(default=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    first_seen = models.DateField()
    last_checked = models.DateField()
    link_type = models.CharField(max_length=20, default='text', choices=[
        ('text', 'Text Link'),
        ('image', 'Image Link'),
        ('redirect', 'Redirect'),
        ('canonical', 'Canonical'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-domain_authority', '-first_seen']
        unique_together = [['source_url', 'target_url']]
        indexes = [
            models.Index(fields=['target_url', '-domain_authority']),
            models.Index(fields=['is_active', '-last_checked']),
        ]

    def __str__(self):
        follow = "Dofollow" if self.is_dofollow else "Nofollow"
        return f"{self.source_url} → {self.target_url} ({follow})"


class ConversionGoal(models.Model):
    """CRO Goals - setup once in admin"""
    GOAL_TYPES = [
        ('click', 'Button Click'),
        ('submit', 'Form Submit'),
        ('download', 'File Download'),
        ('scroll', 'Scroll Depth'),
        ('time', 'Time on Page'),
        ('pageview', 'Page View'),
        ('external_click', 'External Link Click'),
    ]

    name = models.CharField(max_length=255, unique=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_selector = models.CharField(max_length=500, blank=True, help_text="CSS selector or element ID")
    target_url = models.CharField(max_length=500, blank=True, help_text="URL pattern to match")
    target_value = models.CharField(max_length=100, blank=True, help_text="Minimum scroll % or seconds")
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ConversionEvent(models.Model):
    """CRO Events - populated by frontend events via API.

    Current frontend sends `event_type` (pageview/click/submit/etc).
    We store it for analytics today, and keep `goal` nullable so you can
    fully switch to goal-based tracking later without breaking existing data.
    """

    # Optional linkage for future goal-based approach
    goal = models.ForeignKey(ConversionGoal, on_delete=models.CASCADE, related_name='events', null=True, blank=True)

    # Required tracking contract for current implementation
    event_type = models.CharField(max_length=30, db_index=True)
    session_id = models.CharField(max_length=255, db_index=True)
    url = models.URLField()
    referrer = models.URLField(blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['goal', '-timestamp']),
            models.Index(fields=['session_id', '-timestamp']),
        ]

    def __str__(self):
        goal_part = self.goal.name if self.goal_id else 'no-goal'
        return f"{goal_part} - {self.event_type} - {self.timestamp}"


class AICrawlerVisit(models.Model):
    """Passive log of AI crawler/bot visits to site pages, detected via User-Agent"""
    AI_CRAWLERS = [
        # OpenAI
        ("gptbot", "OpenAI GPTBot"),
        ("chatgpt_user", "ChatGPT-User"),
        
        # Anthropic
        ("claudebot", "Anthropic ClaudeBot"),
        ("claude_user", "Claude-User"),
        
        # Google
        ("googlebot", "Googlebot"),
        ("google_extended", "Google-Extended"),
        ("googleother", "GoogleOther"),
        
        # Microsoft
        ("bingbot", "Bingbot"),
        
        # Perplexity
        ("perplexitybot", "PerplexityBot"),
        ("perplexity_user", "Perplexity-User"),
        
        # Amazon
        ("amazonbot", "Amazonbot"),
        
        # Apple
        ("applebot", "Applebot"),
        
        # ByteDance
        ("bytespider", "ByteDance Bytespider"),
        
        # Common AI/Search crawlers
        ("ccbot", "Common Crawl CCBot"),
        ("yandexbot", "YandexBot"),
        ("duckassistbot", "DuckAssistBot"),
        ("facebookbot", "Meta ExternalHit"),
        ("oai_searchbot", "OpenAI SearchBot"),
        
        # Unknown AI crawler
        ("other_ai", "Other AI Crawler"),
    ]

    crawler = models.CharField(max_length=30, choices=AI_CRAWLERS, db_index=True)
    user_agent_raw = models.CharField(max_length=500)
    path = models.CharField(max_length=500)
    host = models.CharField(max_length=255)
    canonical = models.BooleanField(default=True)
    redirected = models.BooleanField(default=False)
    redirect_reason = models.CharField(
        max_length=40,
        blank=True,
        null = True,
        choices=[
            ("deployment_host", "Vercel deployment host"),
            ("custom_redirect", "Application redirect"),
            ("other", "Other"),
        ],
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['crawler', '-timestamp']),
            models.Index(fields=['path', '-timestamp']),
            models.Index(fields=['host', '-timestamp']),
            models.Index(fields=['canonical', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.crawler} → {self.path} @ {self.timestamp}"