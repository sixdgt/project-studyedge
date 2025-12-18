from django.urls import path
from web.views import destination, index, study_abroad_step, faq_details, about_us, services

urlpatterns = [
    path('', index, name='index'),
    path('destinations/australia/', destination, name='australia'),
    path('study-abroad-steps/', study_abroad_step, name='study_abroad_steps'),
    path('faq-details/', faq_details, name='faq_details'),
    path("about-us/", about_us, name="about_us"),
    path("our-services/", services, name="services")
]
