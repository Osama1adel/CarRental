# bookings/views.py (النسخة النهائية)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse 
from .models import Booking # 💡 هذا المودل الآن يحتوي على دالة calculate_prices()
from .forms import BookingForm
from vehicles.models import Car 
# 💡 لا تحتاج لاستيراد logging هنا، فهو في payments/views.py

@login_required(login_url='accounts:login')
def create_booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            
            # 🛑 1. استدعاء دالة حساب الأسعار والمدة صراحةً
            # هذا يضمن أن الحقول total_price و duration_days مُحسَبة الآن
            booking.calculate_prices() 
            
            # 🛑 2. الحفظ بعد الحساب (save() ستعيد استدعاء calculate_prices للتأكيد)
            booking.save() 

            # 3. التوجيه إلى صفحة الدفع ببيانات حجز كاملة ومحفوظة
            return redirect(reverse('payments:initiate_payment', args=[booking.id]))

    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'car': car
    })

# 2. صفحة نجاح الحجز (كود سليم)
@login_required
def booking_success(request):
    return render(request, 'bookings/booking_success.html')

# 3. لوحة تحكم المراجع (كود سليم)
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser) 
def reviewer_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    
    # ... (بقية الدالة سليمة) ...
    
    total_revenue = bookings.filter(status='CONFIRMED').aggregate(Sum('total_price'))['total_price__sum'] or 0

    stats = {
        'total_bookings': bookings.count(),
        'pending_count': bookings.filter(status='PENDING').count(),
        'confirmed_count': bookings.filter(status='CONFIRMED').count(),
        'total_revenue': total_revenue
    }

    context = {
        'bookings': bookings,
        'stats': stats 
    }

    return render(request, 'bookings/reviewer_dashboard.html', context)