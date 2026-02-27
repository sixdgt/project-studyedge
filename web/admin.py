from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import (
    Destination, DestinationSection, BulletPoint, SectionStat,
    TopCourse, TopUniversity, HeroHighlight,
    BlogCategory, BlogTag, BlogPost, BlogComment, 
    CallbackRequest, BookTest, Testimonial, CounsellingAppointment
)

# ========== ADMIN TITLES ==========

admin.site.site_header = "StudyEdge CMS"
admin.site.site_title = "StudyEdge Admin"
admin.site.index_title = "Content Management"
# ========== Page Form ==========
@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ["full_name", "country", "contact_number", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["full_name", "contact_number"]
    
@admin.register(CounsellingAppointment)
class CounsellingAppointmentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "contact_number", "preferred_date", "preferred_time", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["full_name", "email"]

@admin.register(BookTest)
class BookTestAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "contact_number", "preferred_date", "test_type", "test_mode", "confirmation_status", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["full_name", "contact_number"]

# ========== INLINES ==========
class HeroHighlightInline(admin.TabularInline):
    model = HeroHighlight
    extra = 0
    max_num = 4

class TopCourseInline(admin.TabularInline):
    model = TopCourse
    extra = 1

class TopUniversityInline(admin.TabularInline):
    model = TopUniversity
    extra = 1

class BulletPointInline(admin.TabularInline):
    model = BulletPoint
    extra = 1

class SectionStatInline(admin.TabularInline):
    model = SectionStat
    extra = 1

# ========== DESTINATION ADMIN ==========
@admin.register(Destination)
class DestinationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'name',
        'slug',
        'featured_icon',
        'active_icon',
        'order',
        'updated_at',
        'hero_image_preview',
    )

    list_editable = ('order',)
    list_filter = ('is_active', 'featured', 'created_at')
    search_fields = ('name', 'tagline')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)

    inlines = [
        HeroHighlightInline,
        TopCourseInline,
        TopUniversityInline,
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'tagline',
                ('is_active', 'featured'),
                'order',
            )
        }),
        ('Hero Section Design', {
            'fields': (
                ('hero_color_from', 'hero_color_via', 'hero_color_to'),
                ('universities_count', 'work_rights_duration', 'work_hours_limit'),
                'hero_image',
            )
        }),
        ('SEO Settings', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )

    # ===== UI HELPERS =====

    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:8px;" />',
                obj.hero_image.url
            )
        return "—"
    hero_image_preview.short_description = "Hero Image"

    def active_icon(self, obj):
        return "✅" if obj.is_active else "❌"
    active_icon.short_description = "Active"

    def featured_icon(self, obj):
        return "⭐" if obj.featured else "—"
    featured_icon.short_description = "Featured"

# ========== DESTINATION SECTION ADMIN ==========
@admin.register(DestinationSection)
class DestinationSectionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'title',
        'destination',
        'section_type',
        'order',
        'is_active',
    )

    list_filter = ('destination', 'section_type', 'is_active')
    search_fields = ('title', 'content')
    ordering = ('destination', 'order')

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'destination',
                'section_type',
                'title',
                ('is_active', 'order'),
            )
        }),
        ('Styling', {
            'fields': ('icon', 'color_from', 'color_to'),
        }),
        ('Content & Display', {
            'fields': (
                'content',
                ('show_bullet_points', 'show_stats'),
            )
        }),
    )

    inlines = [BulletPointInline, SectionStatInline]

# ========== TESTIMONIALS SECTION ADMIN ==========
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'is_active')
    list_filter = ('is_active',)

# ========== BULLET POINT ADMIN ==========
@admin.register(BulletPoint)
class BulletPointAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('section', 'short_text', 'order')
    list_filter = ('section__destination',)
    search_fields = ('text',)
    ordering = ('order',)

    def short_text(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    short_text.short_description = 'Bullet Text'

# ========== SECTION STAT ADMIN ==========
@admin.register(SectionStat)
class SectionStatAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('section', 'label', 'value', 'color', 'order')
    list_filter = ('section__destination',)
    ordering = ('order',)

# ========== TOP COURSE ADMIN ==========
@admin.register(TopCourse)
class TopCourseAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('destination', 'name', 'order')
    list_filter = ('destination',)
    ordering = ('order',)

# ========== TOP UNIVERSITY ADMIN ==========
@admin.register(TopUniversity)
class TopUniversityAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('destination', 'name', 'ranking', 'order')
    list_filter = ('destination',)
    ordering = ('order',)

# ========== HERO HIGHLIGHT ADMIN ==========
@admin.register(HeroHighlight)
class HeroHighlightAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('destination', 'text', 'order')
    list_filter = ('destination',)
    ordering = ('order',)

# ========== BLOG ADMIN ==========
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'slug', 'is_active', 'order', 'updated_at')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('name', 'email', 'content', 'created_at')
    can_delete = True

@admin.register(BlogPost)
class BlogPostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'featured_image_preview', 'title', 'slug', 'status', 'category', 'is_featured', 'is_trending', 'published_date', 'reading_time'
    )
    list_filter = ('status', 'category', 'is_featured', 'is_trending')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'featured_image_preview', 'author_image_preview')
    date_hierarchy = 'published_date'
    inlines = [BlogCommentInline]
    actions = ['make_published', 'make_draft', 'approve_comments']

    fieldsets = (
        ('Basic', {'fields': ('title', 'slug', 'excerpt', 'category', 'tags', 'related_destination')}),
        ('Media', {'fields': ('featured_image', 'featured_image_alt')}),
        ('Content', {'fields': ('content',)}),
        ('Publishing', {'fields': ('status', 'published_date', 'is_featured', 'is_trending', 'allow_comments')}),
        ('Author & SEO', {'fields': ('author_name', 'author_image', 'author_bio', 'meta_description', 'meta_keywords')}),
        ('Stats', {'fields': ('views_count', 'reading_time')}),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="90" style="border-radius:6px;" />', obj.featured_image.url)
        return "—"
    featured_image_preview.short_description = "Featured Image"

    def author_image_preview(self, obj):
        if obj.author_image:
            return format_html('<img src="{}" width="50" style="border-radius:50%;" />', obj.author_image.url)
        return "—"
    author_image_preview.short_description = "Author Image"

    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f"{updated} post(s) marked as published.")
    make_published.short_description = "Mark selected posts as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f"{updated} post(s) marked as draft")
    make_draft.short_description = "Mark selected posts as draft"

    def approve_comments(self, request, queryset):
        count = 0
        for post in queryset:
            updated = post.comments.filter(is_approved=False).update(is_approved=True)
            count += updated
        self.message_user(request, f"{count} comment(s) approved for selected posts.")
    approve_comments.short_description = "Approve all comments for selected posts"

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = ('name', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'content', 'post__title')
    readonly_fields = ('created_at',)
    actions = ['approve_comments_action']

    def approve_comments_action(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments_action.short_description = "Approve selected comments"
