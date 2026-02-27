from django.db import models
from django.utils.text import slugify
from django_ckeditors.fields import CKEditorsField  # Optional: for rich text content

class Destination(models.Model):
    """Main destination country model"""
    
    # Basic Info
    name = models.CharField(max_length=100, help_text="e.g., Australia, United Kingdom")
    slug = models.SlugField(unique=True, max_length=100, help_text="URL-friendly name (e.g., australia, uk)")
    tagline = models.CharField(max_length=300, help_text="Subtitle for hero section")
    
    # Hero Section Colors (Tailwind classes without prefix)
    hero_color_from = models.CharField(max_length=50, default='blue-600', 
                                       help_text="Start gradient color (e.g., blue-600)")
    hero_color_via = models.CharField(max_length=50, default='blue-700',
                                      help_text="Middle gradient color (e.g., blue-700)")
    hero_color_to = models.CharField(max_length=50, default='indigo-800',
                                     help_text="End gradient color (e.g., indigo-800)")
    
    # Hero Stats
    universities_count = models.CharField(max_length=50, help_text="e.g., 43, 130+")
    work_rights_duration = models.CharField(max_length=50, help_text="e.g., 2-4 Yrs")
    work_hours_limit = models.CharField(max_length=50, help_text="e.g., 48h, 20h/week")
    
    # Hero Image (optional)
    hero_image = models.ImageField(upload_to='destinations/hero/', blank=True, null=True)
    
    # Meta
    meta_description = models.TextField(max_length=160, blank=True, 
                                       help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True,
                                    help_text="SEO keywords, comma-separated")
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Show on website")
    featured = models.BooleanField(default=False, help_text="Featured destination")
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('destination_detail', kwargs={'slug': self.slug})

class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='testimonials/')
    quote = models.TextField()
    university = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    intake = models.CharField(max_length=100)

    border_color = models.CharField(max_length=50, default="border-blue-500")
    text_color = models.CharField(max_length=100, default="text-blue-700 dark:text-blue-300")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DestinationSection(models.Model):
    """Content sections for each destination"""
    
    SECTION_TYPES = [
        ('why_study', 'Why Study Here'),
        ('visa_requirements', 'Visa Requirements'),
        ('cost', 'Cost of Studying'),
        ('scholarships', 'Scholarships'),
        ('intakes', 'Intakes'),
        ('language_requirements', 'Language Requirements (IELTS/PTE)'),
        ('top_courses', 'Top Courses'),
        ('top_universities', 'Top Universities'),
        ('job_prospects', 'Job Prospects'),
        ('living_costs', 'Cost of Living'),
        ('accommodation', 'Accommodation Options'),
        ('culture', 'Culture & Lifestyle'),
        ('application_process', 'Application Process'),
        ('faqs', 'FAQs'),
        ('custom', 'Custom Section'),
    ]
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, 
                                   related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    title = models.CharField(max_length=200, help_text="Section heading")
    
    # Icon (FontAwesome class without 'fas')
    icon = models.CharField(max_length=50, default='fa-globe', 
                           help_text="FontAwesome icon (e.g., fa-globe, fa-passport)")
    
    # Colors for section number badge
    color_from = models.CharField(max_length=50, default='blue-500',
                                 help_text="Badge gradient start (e.g., blue-500)")
    color_to = models.CharField(max_length=50, default='indigo-600',
                               help_text="Badge gradient end (e.g., indigo-600)")
    
    # Content
    content = CKEditorsField(blank=True, help_text="Main section content (HTML allowed)")
    # If not using CKEditor, use: content = models.TextField(blank=True)
    
    # Display
    show_bullet_points = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=False)
    show_mini_cards = models.BooleanField(default=False, help_text="Show mini info cards")
    order = models.IntegerField(default=0, help_text="Section order")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Destination Section'
        verbose_name_plural = 'Destination Sections'
    
    def __str__(self):
        return f"{self.destination.name} - {self.title}"

class BulletPoint(models.Model):
    """Bullet points for sections (e.g., visa requirements list)"""
    
    section = models.ForeignKey(DestinationSection, on_delete=models.CASCADE,
                               related_name='bullet_points')
    text = models.TextField(help_text="Bullet point content")
    icon = models.CharField(max_length=50, default='fa-check-circle',
                           help_text="FontAwesome icon (e.g., fa-check-circle)")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Bullet Point'
        verbose_name_plural = 'Bullet Points'
    
    def __str__(self):
        return f"{self.section.title} - {self.text[:50]}"

class MiniCard(models.Model):
    """Mini info cards for sections (compact visual information blocks)"""
    
    section = models.ForeignKey(DestinationSection, on_delete=models.CASCADE,
                               related_name='mini_cards')
    title = models.CharField(max_length=100, help_text="Card title (e.g., Student Visa)")
    subtitle = models.CharField(max_length=150, blank=True, 
                               help_text="Small text below title (e.g., Subclass 500)")
    description = models.TextField(help_text="Card description (2-3 lines)")
    
    icon = models.CharField(max_length=50, default='fa-info-circle',
                           help_text="FontAwesome icon")
    
    # Styling
    bg_color = models.CharField(max_length=50, default='blue-50',
                               help_text="Background color (e.g., blue-50, green-50)")
    icon_color = models.CharField(max_length=50, default='blue-600',
                                 help_text="Icon color (e.g., blue-600)")
    border_color = models.CharField(max_length=50, default='blue-200',
                                   help_text="Border color (e.g., blue-200)")
    
    # Optional link
    link_text = models.CharField(max_length=50, blank=True, 
                                help_text="Link text (e.g., Learn More)")
    link_url = models.URLField(blank=True, help_text="External link URL")
    
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Mini Card'
        verbose_name_plural = 'Mini Cards'
    
    def __str__(self):
        return f"{self.section.title} - {self.title}"

class SectionStat(models.Model):
    """Stats/cards for sections (e.g., tuition fees, living costs)"""
    
    section = models.ForeignKey(DestinationSection, on_delete=models.CASCADE,
                               related_name='stats')
    label = models.CharField(max_length=100, help_text="Stat label (e.g., Tuition Fees)")
    value = models.CharField(max_length=100, help_text="Stat value (e.g., AUD 20K-45K)")
    description = models.CharField(max_length=200, blank=True,
                                  help_text="Small text below value (e.g., Per year)")
    
    icon = models.CharField(max_length=50, default='fa-info-circle',
                           help_text="FontAwesome icon")
    color = models.CharField(max_length=50, default='blue-600',
                            help_text="Color theme (e.g., blue-600, green-600)")
    
    # Layout
    column_span = models.IntegerField(default=1, choices=[(1, '1 Column'), (2, '2 Columns')],
                                     help_text="Grid column span")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Section Stat'
        verbose_name_plural = 'Section Stats'
    
    def __str__(self):
        return f"{self.section.title} - {self.label}: {self.value}"

class TopCourse(models.Model):
    """Popular courses for a destination"""
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,
                                   related_name='top_courses')
    name = models.CharField(max_length=200, help_text="Course name")
    icon = models.CharField(max_length=50, default='fa-graduation-cap')
    color = models.CharField(max_length=50, default='blue-600',
                            help_text="Background color (e.g., blue-50)")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Top Course'
        verbose_name_plural = 'Top Courses'
    
    def __str__(self):
        return f"{self.destination.name} - {self.name}"

class TopUniversity(models.Model):
    """Top universities for a destination"""
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,
                                   related_name='top_universities')
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='destinations/universities/', blank=True, null=True)
    ranking = models.CharField(max_length=100, blank=True, help_text="e.g., #1 in Australia")
    website = models.URLField(blank=True)
    
    color = models.CharField(max_length=50, default='blue-600')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Top University'
        verbose_name_plural = 'Top Universities'
    
    def __str__(self):
        return f"{self.destination.name} - {self.name}"

class HeroHighlight(models.Model):
    """4 highlight points in the hero section (Why study here?)"""
    
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE,
                                   related_name='hero_highlights')
    text = models.CharField(max_length=100, help_text="e.g., World-class education")
    icon = models.CharField(max_length=50, default='fa-check-circle')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Highlight'
        verbose_name_plural = 'Hero Highlights'
    
    def __str__(self):
        return f"{self.destination.name} - {self.text}"


# ============================================================================
# BLOG MODELS
# ============================================================================

class BlogCategory(models.Model):
    """Blog categories/topics"""
    
    name = models.CharField(max_length=100, help_text="e.g., Study Abroad Tips, Visa Guide")
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    
    # Styling
    color = models.CharField(max_length=50, default='blue-600',
                            help_text="Category color (e.g., blue-600)")
    icon = models.CharField(max_length=50, default='fa-folder',
                           help_text="FontAwesome icon")
    
    # Meta
    meta_description = models.TextField(max_length=160, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_category', kwargs={'slug': self.slug})


class BlogTag(models.Model):
    """Tags for blog posts"""
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Main blog post model"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    excerpt = models.TextField(max_length=300, help_text="Short summary for listings")
    
    # Content
    content = CKEditorsField(help_text="Main blog content (HTML allowed)")
    # If not using CKEditor, use: content = models.TextField()
    
    # Media
    featured_image = models.ImageField(upload_to='blog/featured/', 
                                      help_text="Main image for the post")
    featured_image_alt = models.CharField(max_length=200, blank=True,
                                         help_text="Alt text for SEO")
    
    # Categorization
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, 
                                null=True, related_name='posts')
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts')
    related_destination = models.ForeignKey(Destination, on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='blog_posts',
                                           help_text="Link to a destination if relevant")
    
    # Author (optional - can be extended with User model)
    author_name = models.CharField(max_length=100, default='Admin')
    author_image = models.ImageField(upload_to='blog/authors/', blank=True, null=True)
    author_bio = models.TextField(max_length=200, blank=True)
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True,
                                         help_text="Date to publish (can be future)")
    
    # Engagement
    views_count = models.IntegerField(default=0, help_text="Number of views")
    reading_time = models.IntegerField(default=5, help_text="Estimated reading time in minutes")
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Features
    is_featured = models.BooleanField(default=False, 
                                     help_text="Show on homepage featured section")
    is_trending = models.BooleanField(default=False,
                                     help_text="Show in trending section")
    allow_comments = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class BlogComment(models.Model):
    """Comments on blog posts (optional)"""
    
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                            related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=False,
                                     help_text="Approve comment to show publicly")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'
    
    def __str__(self):
        return f"{self.name} on {self.post.title}"


# ============================================================================
# EXISTING FORM MODELS
# ============================================================================

class BookTest(models.Model):
    TEST_CHOICES = [
        ('IELTS Academic', 'IELTS Academic'),
        ('IELTS CBT', 'IELTS CBT'), 
        ('IELTS UKVI', 'IELTS UKVI'),
        ('IELTS General', 'IELTS General'),
        ('PTE Academic', 'PTE Academic'),
        ('PTE Academic UKVI', 'PTE Academic UKVI'),
        ('PTE Core', 'PTE Core'),
        ('OET', 'OET'),
        ('Duolingo Test', 'Duolingo Test'),
    ]
    MODE_CHOICES = [
        ('In-Person', 'In-Person'),
        ('Online', 'Online'),
    ]
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    contact_number = models.CharField(max_length=20)
    preferred_date = models.DateField()
    test_type = models.CharField(choices=TEST_CHOICES, max_length=50)
    test_mode = models.CharField(choices=MODE_CHOICES, max_length=50)
    confirmation_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Book Tests'

    def __str__(self):
        return f"{self.full_name} - {self.test_type} on {self.preferred_date}"
    
class CallbackRequest(models.Model):
    full_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Callback Requests'

    def __str__(self):
        return f"{self.full_name} - {self.contact_number}"

class CounsellingAppointment(models.Model):
    DESTINATION_CHOICES = [
        ('Australia', 'Australia'),
        ('Canada', 'Canada'),
        ('UK', 'UK'),
        ('USA', 'USA'),
        ('Germany', 'Germany'),
        ('New Zealand', 'New Zealand'),
        ('France', 'France'),
        ('Other', 'Other'),
    ]
    
    CURRENT_ACADEMIC_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('bachelors', "Bachelor's"),
        ('masters', "Master's"),
    ]
    
    ACADEMIC_LEVEL_CHOICES = [
        ('bachelors', "Bachelor's"),
        ('masters', "Master's"),
        ('phd', 'PhD'),
    ]
    
    MODE_CHOICES = [
        ('online', 'Online (Video Call)'),
        ('in_person', 'In-Person Visit'),
        ('phone', 'Phone Call'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    preferred_destination = models.CharField(choices=DESTINATION_CHOICES, max_length=50)
    intended_academic_level = models.CharField(choices=ACADEMIC_LEVEL_CHOICES, max_length=50)
    current_academic_level = models.CharField(choices=CURRENT_ACADEMIC_LEVEL_CHOICES, max_length=50)
    counselling_mode = models.CharField(choices=MODE_CHOICES, max_length=20)
    accept_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Counselling Appointments'

    def __str__(self):
        return f"{self.full_name} - {self.preferred_date} at {self.preferred_time}"