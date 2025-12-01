from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # رابط الحجز يحتاج معرف السيارة
    path('create/<int:car_id>/', views.create_booking, name='create_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('dashboard/', views.reviewer_dashboard, name='reviewer_dashboard'),
]