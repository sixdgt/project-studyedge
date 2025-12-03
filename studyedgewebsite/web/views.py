from django.shortcuts import render
from web.forms import CounsellingAppointmentForm
# Create your views here.
def index(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Study Edge help you in every step."
    return render(request, 'index.html', {'student_support_title': student_support_title, 'form': form})

def destination(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Find your perfect study destination with StudyEdge"
    return render(request, 'destinations/destination_detail.html', {'student_support_title': student_support_title, 'form': form})

def study_abroad_step(request):
    form = CounsellingAppointmentForm()
    student_support_title = "Applying made easy with StudyEdge"
    return render(request, 'study_abroad_steps.html', {'student_support_title': student_support_title, 'form': form})