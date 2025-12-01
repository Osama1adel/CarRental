from django.urls import path
from . import views

app_name = "name"
urlpatterns = [
    path("booking_success/", views.booking_success, name="booking_success"),
    path("create_booking/", views.create_booking, name="create_booking"),
    path("reviewer_dashboard/", views.reviewer_dashboard, name="reviewer_dashboard"),

]