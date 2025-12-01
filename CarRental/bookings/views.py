from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def booking_success(request):
    return render(request, 'booking_success.html')

def create_booking(request):
    return render(request, 'create_booking.html')

def reviewer_dashboard(request):
    return render(request, 'reviewer_dashboard.html')
