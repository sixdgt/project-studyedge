from django.shortcuts import render, redirect
from web.forms import CounsellingAppointmentForm, BookTestForm, CallbackRequestForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages
from web.models import Destination, BlogPost, BlogCategory, BlogTag, BlogComment, Testimonial
from django.shortcuts import render, get_object_or_404
from django.http import Http404


# ─────────────────────────────────────────────
# Shared helper: builds the common context that
# every page using the counselling form needs.
# ─────────────────────────────────────────────
def _common_context(form=None):
    return {
        'form': form or CounsellingAppointmentForm(),
        'book_test_form': BookTestForm(),
        'callback_request_form': CallbackRequestForm(),
        'destinations': Destination.objects.filter(is_active=True)[:7],
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('-created_at'),
    }


# ─────────────────────────────────────────────
# PAGE → TEMPLATE map  (add new pages here)
# ─────────────────────────────────────────────
PAGE_TEMPLATES = {
    'index':              ('index.html',              "Study Edge help you in every step."),
    'our-services':       ('services.html',           "Study Edge might be your best guide to achieve your goal."),
    'destinations':       ('destinations/destination_list.html', "Find your perfect destination."),
    'study-abroad-steps': ('study_abroad_steps.html', "Applying made easy with StudyEdge"),
    'about-us':           ('about_us.html',           "Study Edge might be your best guide to achieve your goal."),
    'faq-details':        ('faq_details.html',        "Study Edge makes your path easy. Apply now!"),
    'blogs':              ('blog/blog_list.html',     "Study Edge help you in every step."),
}


# ─────────────────────────────────────────────
# INDEX
# ─────────────────────────────────────────────
def index(request):
    context = _common_context()
    context['student_support_title'] = "Study Edge help you in every step."
    return render(request, 'index.html', context)


# ─────────────────────────────────────────────
# COUNSELLING APPOINTMENT  (handles all pages)
# ─────────────────────────────────────────────
def counselling_appointment(request):
    if request.method == "POST":
        form = CounsellingAppointmentForm(request.POST)
        current_page = request.POST.get('current_page', 'index')
        template, support_title = PAGE_TEMPLATES.get(
            current_page, ('index.html', "Study Edge help you in every step.")
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been booked successfully!")
            # Go back to the exact page the user was on
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        # ── Validation failed ──────────────────────────────────────────
        messages.error(request, "Please correct the errors below.")
        context = _common_context(form=form)          # ✅ bound form keeps values + errors
        context['student_support_title'] = support_title
        context['scroll_to_counselling_form'] = True  # triggers auto-scroll in template
        return render(request, template, context)

    return redirect("index")


# ─────────────────────────────────────────────
# CALLBACK REQUEST
# ─────────────────────────────────────────────
def call_back_request(request):
    if request.method == "POST":
        data = CallbackRequestForm(request.POST)
        if data.is_valid():
            data.save()
            messages.success(request, "Your request has been submitted!")
        else:
            messages.error(request, "Failed to send your request!")
    return redirect(request.META.get('HTTP_REFERER', 'index'))


# ─────────────────────────────────────────────
# BOOK TEST
# ─────────────────────────────────────────────
def book_test(request):
    if request.method == "POST":
        form = BookTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been submitted!")
        else:
            messages.error(request, "Please correct the errors below.")
    return redirect(request.META.get('HTTP_REFERER', 'index'))


# ─────────────────────────────────────────────
# DESTINATIONS
# ─────────────────────────────────────────────
def destination_list(request):
    destinations = Destination.objects.filter(is_active=True)
    context = _common_context()
    context.update({
        'destinations': destinations,
        'featured_destinations': destinations.filter(featured=True)[:3],
        'student_support_title': "Find your perfect destination.",
    })
    return render(request, 'destinations/destination_list.html', context)


def destination_detail(request, slug):
    destination = get_object_or_404(
        Destination.objects.prefetch_related(
            'sections', 'sections__bullet_points', 'sections__stats',
            'top_courses', 'top_universities', 'hero_highlights'
        ),
        slug=slug, is_active=True
    )
    context = {
        'destination': destination,
        'sections': destination.sections.filter(is_active=True),
        'top_courses': destination.top_courses.all(),
        'top_universities': destination.top_universities.all(),
        'hero_highlights': destination.hero_highlights.all(),
        'meta_title': f"Study in {destination.name} | StudyEdge Experts",
        'meta_description': destination.meta_description or destination.tagline,
        'meta_keywords': destination.meta_keywords,
    }
    return render(request, 'destinations/destination_detail.html', context)


# ─────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────
def blog_list(request):
    posts = BlogPost.objects.filter(
        status='published', published_date__lte=timezone.now()
    ).select_related('category').prefetch_related('tags')

    search_query   = request.GET.get('search', '')
    category_slug  = request.GET.get('category', '')
    tag_slug       = request.GET.get('tag', '')
    destination_slug = request.GET.get('destination', '')
    sort_by        = request.GET.get('sort', '-published_date')

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    if destination_slug:
        posts = posts.filter(related_destination__slug=destination_slug)

    valid_sorts = ['-published_date', 'published_date', '-views_count', 'title']
    if sort_by in valid_sorts:
        posts = posts.order_by(sort_by)

    paginator  = Paginator(posts, 9)
    page_obj   = paginator.get_page(request.GET.get('page'))
    categories = BlogCategory.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    popular_tags = BlogTag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-post_count')[:10]
    recent_posts = BlogPost.objects.filter(
        status='published', published_date__lte=timezone.now()
    ).order_by('-published_date')[:5]
    featured_posts = BlogPost.objects.filter(
        status='published', is_featured=True, published_date__lte=timezone.now()
    ).order_by('-published_date')[:3]

    context = _common_context()
    context.update({
        'page_obj': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'recent_posts': recent_posts,
        'featured_posts': featured_posts,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'current_destination': destination_slug,
        'sort_by': sort_by,
        'student_support_title': "Study Edge help you in every step.",
    })
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related('category', 'related_destination')
                        .prefetch_related('tags', 'comments'),
        slug=slug, status='published', published_date__lte=timezone.now()
    )
    post.increment_views()
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    related_posts = BlogPost.objects.filter(
        status='published', published_date__lte=timezone.now()
    ).filter(
        Q(category=post.category) | Q(tags__in=post.tags.all())
    ).exclude(id=post.id).distinct().order_by('-published_date')[:3]

    previous_post = BlogPost.objects.filter(
        status='published', published_date__lt=post.published_date
    ).order_by('-published_date').first()
    next_post = BlogPost.objects.filter(
        status='published', published_date__gt=post.published_date
    ).order_by('published_date').first()

    context = {
        'post': post, 'comments': comments,
        'related_posts': related_posts,
        'previous_post': previous_post, 'next_post': next_post,
    }
    return render(request, 'blog/blog_detail.html', context)


def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    posts    = BlogPost.objects.filter(
        category=category, status='published', published_date__lte=timezone.now()
    ).order_by('-published_date')
    paginator = Paginator(posts, 9)
    categories = BlogCategory.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    context = {
        'category': category,
        'page_obj': paginator.get_page(request.GET.get('page')),
        'categories': categories,
    }
    return render(request, 'blog/blog_category.html', context)


def blog_tag(request, slug):
    tag   = get_object_or_404(BlogTag, slug=slug)
    posts = BlogPost.objects.filter(
        tags=tag, status='published', published_date__lte=timezone.now()
    ).order_by('-published_date')
    paginator = Paginator(posts, 9)
    context = {
        'tag': tag,
        'page_obj': paginator.get_page(request.GET.get('page')),
    }
    return render(request, 'blog/blog_tag.html', context)


def blog_search(request):
    query = request.GET.get('q', '').strip()
    posts = BlogPost.objects.filter(
        status='published', published_date__lte=timezone.now()
    ).filter(
        Q(title__icontains=query) | Q(excerpt__icontains=query) |
        Q(content__icontains=query) | Q(category__name__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct().order_by('-published_date') if query else BlogPost.objects.none()

    paginator = Paginator(posts, 9)
    context = {
        'query': query,
        'page_obj': paginator.get_page(request.GET.get('page')),
        'results_count': posts.count(),
    }
    return render(request, 'blog/blog_search.html', context)


def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        if not post.allow_comments:
            messages.error(request, 'Comments are disabled for this post.')
            return redirect('blog_detail', slug=slug)
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        content = request.POST.get('content', '').strip()
        if name and email and content:
            BlogComment.objects.create(
                post=post, name=name, email=email,
                content=content, is_approved=False
            )
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
        else:
            messages.error(request, 'Please fill in all fields.')
    return redirect('blog_detail', slug=slug)


# ─────────────────────────────────────────────
# OTHER PAGES
# ─────────────────────────────────────────────
def study_abroad_step(request):
    context = _common_context()
    context['student_support_title'] = "Applying made easy with StudyEdge"
    return render(request, 'study_abroad_steps.html', context)


def faq_details(request):
    context = _common_context()
    context['student_support_title'] = "Study Edge makes your path easy. Apply now!"
    return render(request, 'faq_details.html', context)


def about_us(request):
    context = _common_context()
    context['student_support_title'] = "Study Edge might be your best guide to achieve your goal."
    return render(request, "about_us.html", context)


def services(request):
    context = _common_context()
    context['student_support_title'] = "Study Edge might be your best guide to achieve your goal."
    return render(request, "services.html", context)