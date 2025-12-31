from django.shortcuts import render
from web.forms import CounsellingAppointmentForm, BookTestForm, CallbackRequestForm
from web.models import Destination
from django.shortcuts import render, get_object_or_404
from django.http import Http404
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