from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import (
    Destination, DestinationSection, BulletPoint, SectionStat,
    TopCourse, TopUniversity, HeroHighlight
)

# ========== ADMIN TITLES ==========

admin.site.site_header = "StudyEdge CMS"
admin.site.site_title = "StudyEdge Admin"
admin.site.index_title = "Content Management"

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
