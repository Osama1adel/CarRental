from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from vehicles.models import Car 

# 1. صفحة إنشاء الحجز
@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save() # سيتم حساب السعر تلقائياً هنا بناءً على المودل
            return redirect('bookings:booking_success')
    else:
        form = BookingForm()

    context = {
        'form': form,
        'car': car
    }
    return render(request, 'bookings/create_booking.html', context)

# 2. صفحة نجاح الحجز
@login_required
def booking_success(request):
    return render(request, 'bookings/booking_success.html')

# 3. لوحة تحكم المراجع (للموظفين فقط)
@login_required
@user_passes_test(lambda u: u.is_staff) # فقط المشرفين يدخلون هنا
def reviewer_dashboard(request):
    # عرض الحجوزات، الأحدث أولاً
    bookings = Booking.objects.all().order_by('-created_at')
    
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(Booking, id=booking_id)
        
        if action == 'approve':
            booking.status = 'CONFIRMED'
            messages.success(request, f'تم قبول الحجز رقم {booking.id}')
        elif action == 'reject':
            booking.status = 'CANCELLED'
            messages.warning(request, f'تم رفض الحجز رقم {booking.id}')
        
        booking.save()
        return redirect('bookings:reviewer_dashboard')

    return render(request, 'bookings/reviewer_dashboard.html', {'bookings': bookings})