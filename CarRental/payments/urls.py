from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.paylink_callback, name='paylink_callback'),
    path('success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]