from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.auth_page, name='auth_page'),
    path('contact/', views.contact, name='contact'),
    path('about-us/', views.about_us, name='about_us'),
    path('careers/', views.careers, name='careers'),
    path("faq/", views.faq_page, name="faq"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
    path('dashboard/messages/', views.contact_messages_dashboard, name='contact_messages_dashboard'),
]