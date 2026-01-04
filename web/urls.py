from django.urls import path
from web.views import (
        index, study_abroad_step, faq_details, about_us,services, 
        destination_list, destination_detail, blog_list, blog_category, 
        blog_search, blog_tag, add_comment, blog_detail,
        call_back_request, book_test
    )

urlpatterns = [
    path('', index, name='index'),
    path('study-abroad-steps/', study_abroad_step, name='study_abroad_steps'),
    path('faq-details/', faq_details, name='faq_details'),
    path("about-us/", about_us, name="about_us"),
    path("our-services/", services, name="services"),
    # call back request
    path('call-back-request/', call_back_request, name="call_back_request"),
    path('book-test/', book_test, name="book_test"),
    # destination pages
    path('destinations/', destination_list, name='destination_list'),
    path('destinations/<slug:slug>/', destination_detail, name='destination_detail'),

    # blogs
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/search/', blog_search, name='blog_search'),
    
    # Category and tag filtering
    path('blogs/category/<slug:slug>/', blog_category, name='blog_category'),
    path('blogs/tag/<slug:slug>/', blog_tag, name='blog_tag'),
    
    # Post detail and comments
    path('blogs/<slug:slug>/', blog_detail, name='blog_detail'),
    path('blogs/<slug:slug>/comment/', add_comment, name='add_comment'),
]
