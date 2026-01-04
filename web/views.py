from django.shortcuts import render, redirect
from web.forms import CounsellingAppointmentForm, BookTestForm, CallbackRequestForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages
from web.models import Destination, BlogPost, BlogCategory, BlogTag, BlogComment
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib import messages

# Create your views here.
def index(request):
    destinations = Destination.objects.filter(is_active=True)[:7]
    book_test_form = BookTestForm()
    form = CounsellingAppointmentForm()
    callback_request_form = CallbackRequestForm()
    student_support_title = "Study Edge help you in every step."
    return render(request, 'index.html', 
                  {'student_support_title': student_support_title,
                    'form': form, 'book_test_form': book_test_form,
                      'callback_request_form': callback_request_form,
                      'destinations': destinations,})

def call_back_request(request):
    if request.method == "POST":
        data = CallbackRequestForm(request.POST)
        if data.is_valid():
            data.save()
            messages.add_message(request, messages.SUCCESS, "Your request has been submitted!!")
            return redirect("index")
        else:
            messages.add_message(request, messages.ERROR, "Failed to send your request!!")
            return redirect("index")

def book_test(request):
    if request.method == "POST":
        form = BookTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been submitted!!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect("index")

def destination_list(request):
    """List all active destinations"""
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'destinations': destinations,
        'featured_destinations': destinations.filter(featured=True)[:3],
    }
    
    return render(request, 'destinations/destination_list.html', context)

def destination_detail(request, slug):
    """Single destination detail page"""
    destination = get_object_or_404(
        Destination.objects.prefetch_related(
            'sections',
            'sections__bullet_points',
            'sections__stats',
            'top_courses',
            'top_universities',
            'hero_highlights'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get only active sections
    sections = destination.sections.filter(is_active=True)
    
    context = {
        'destination': destination,
        'sections': sections,
        'top_courses': destination.top_courses.all(),
        'top_universities': destination.top_universities.all(),
        'hero_highlights': destination.hero_highlights.all(),
        
        # SEO
        'meta_title': f"Study in {destination.name} | StudyEdge Experts",
        'meta_description': destination.meta_description or destination.tagline,
        'meta_keywords': destination.meta_keywords,
    }
    
    return render(request, 'destinations/destination_detail.html', context)

# for blogs
def blog_list(request):
    """Main blog listing page with filters"""
    
    # Get all published posts
    posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).select_related('category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Tag filter
    tag_slug = request.GET.get('tag', '')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Destination filter
    destination_slug = request.GET.get('destination', '')
    if destination_slug:
        posts = posts.filter(related_destination__slug=destination_slug)
    
    # Sorting
    sort_by = request.GET.get('sort', '-published_date')
    valid_sorts = ['-published_date', 'published_date', '-views_count', 'title']
    if sort_by in valid_sorts:
        posts = posts.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(posts, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = BlogCategory.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    popular_tags = BlogTag.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-post_count')[:10]
    
    recent_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')[:5]
    
    featured_posts = BlogPost.objects.filter(
        status='published',
        is_featured=True,
        published_date__lte=timezone.now()
    ).order_by('-published_date')[:3]
    
    context = {
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
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Individual blog post detail page"""
    
    post = get_object_or_404(
        BlogPost.objects.select_related('category', 'related_destination')
                       .prefetch_related('tags', 'comments'),
        slug=slug,
        status='published',
        published_date__lte=timezone.now()
    )
    
    # Increment view count
    post.increment_views()
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    
    # Related posts (same category or tags)
    related_posts = BlogPost.objects.filter(
        status='published',
        published_date__lte=timezone.now()
    ).filter(
        Q(category=post.category) | Q(tags__in=post.tags.all())
    ).exclude(id=post.id).distinct().order_by('-published_date')[:3]
    
    # Previous and next posts
    previous_post = BlogPost.objects.filter(
        status='published',
        published_date__lt=post.published_date
    ).order_by('-published_date').first()
    
    next_post = BlogPost.objects.filter(
        status='published',
        published_date__gt=post.published_date
    ).order_by('published_date').first()
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, slug):
    """Posts filtered by category"""
    
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    
    posts = BlogPost.objects.filter(
        category=category,
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for sidebar
    categories = BlogCategory.objects.filter(is_active=True).annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    )
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    
    return render(request, 'blog/blog_category.html', context)

def blog_tag(request, slug):
    """Posts filtered by tag"""
    
    tag = get_object_or_404(BlogTag, slug=slug)
    
    posts = BlogPost.objects.filter(
        tags=tag,
        status='published',
        published_date__lte=timezone.now()
    ).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    
    return render(request, 'blog/blog_tag.html', context)

def blog_search(request):
    """Search results page"""
    
    query = request.GET.get('q', '').strip()
    
    if query:
        posts = BlogPost.objects.filter(
            status='published',
            published_date__lte=timezone.now()
        ).filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    else:
        posts = BlogPost.objects.none()
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'results_count': posts.count(),
    }
    
    return render(request, 'blog/blog_search.html', context)

def add_comment(request, slug):
    """Handle comment submission"""
    
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        
        if not post.allow_comments:
            messages.error(request, 'Comments are disabled for this post.')
            return redirect('blog_detail', slug=slug)
        
        # Create comment
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        content = request.POST.get('content', '').strip()
        
        if name and email and content:
            BlogComment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content,
                is_approved=False  # Requires moderation
            )
            messages.success(
                request, 
                'Your comment has been submitted and is awaiting moderation.'
            )
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return redirect('blog_detail', slug=slug)

def study_abroad_step(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Applying made easy with StudyEdge"
    return render(request, 'study_abroad_steps.html', {'student_support_title': student_support_title, 'form': form})

def faq_details(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Study Edge makes your path easy. Apply now!"
    return render(request, 'faq_details.html', {'student_support_title': student_support_title, 'form': form})

def about_us(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Study Edge might be your best guide to achieve your goal."
    return render(request, "about_us.html", {'student_support_title': student_support_title, 'form': form})

def services(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Study Edge might be your best guide to achieve your goal."
    return render(request, "services.html", {'student_support_title': student_support_title, 'form': form})