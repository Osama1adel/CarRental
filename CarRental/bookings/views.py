# bookings/views.py (المحتوى الكامل والمعدل)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse # 💡 هذا الاستيراد مهم لاستخدام reverse()
from .models import Booking
from .forms import BookingForm
from vehicles.models import Car 

# 1. صفحة إنشاء الحجز (المُعدَّلة للتوجيه إلى الدفع)
@login_required
def create_booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            
            # سيتم حفظ السعر الإجمالي هنا بناءً على دالة save() في مودل Booking
            booking.save() 
            
            # ✨ نقطة الدمج والتوجيه إلى تطبيق payments ✨
            # نوجه العميل إلى مسار 'initiate_payment' في مساحة الاسم 'payments'
            return redirect(reverse('payments:initiate_payment', args=[booking.id]))
            
    else:
        form = BookingForm()

    context = {
        'form': form,
        'car': car
    }
    return render(request, 'bookings/create_booking.html', context)

# 2. صفحة نجاح الحجز (ستبقى للاستخدام إذا قررت عدم إلغائها)
@login_required
def booking_success(request):
    return render(request, 'bookings/booking_success.html')

# 3. لوحة تحكم المراجع (للموظفين فقط) - (لم تتغير)
@login_required
@user_passes_test(lambda u: u.is_staff) 
def reviewer_dashboard(request):
    # عرض الحجوزات، الأحدث أولاً
    bookings = Booking.objects.all().order_by('-created_at')
    
    # --- معالجة قبول أو رفض الحجز (POST) ---
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(Booking, id=booking_id)
        
        if action == 'approve':
            booking.status = 'CONFIRMED'
            messages.success(request, f'Booking #{booking.id} Approved')
        elif action == 'reject':
            booking.status = 'CANCELLED'
            messages.warning(request, f'Booking #{booking.id} Rejected')
        
        booking.save()
        return redirect('bookings:reviewer_dashboard')

    # --- ✨ حساب الإحصائيات للداشبورد ✨ ---
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