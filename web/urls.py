from django.urls import path
from web.views import destination, index, study_abroad_step, faq_details

urlpatterns = [
    path('', index, name='index'),
    path('destinations/australia/', destination, name='australia'),
    path('study-abroad-steps/', study_abroad_step, name='study_abroad_steps'),
    path('faq-details/', faq_details, name='faq_details'),
]
