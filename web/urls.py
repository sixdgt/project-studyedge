from django.urls import path
from web.views import index, study_abroad_step, faq_details, about_us,services, destination_list, destination_detail

urlpatterns = [
    path('', index, name='index'),
    path('study-abroad-steps/', study_abroad_step, name='study_abroad_steps'),
    path('faq-details/', faq_details, name='faq_details'),
    path("about-us/", about_us, name="about_us"),
    path("our-services/", services, name="services"),

    # destination pages
    path('destinations/', destination_list, name='destination_list'),
    path('destinations/<slug:slug>/', destination_detail, name='destination_detail'),
]
