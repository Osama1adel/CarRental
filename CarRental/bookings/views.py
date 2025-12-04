# bookings/views.py (المحتوى الكامل والمعدل)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Q
from django.urls import reverse # 💡 هذا الاستيراد مهم لاستخدام reverse()
from .models import Booking
from .forms import BookingForm
from vehicles.models import Car 


@login_required(login_url='accounts:login')
def create_booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        # ✅ نرسل car.id للفورم لكي يتمكن من فحص التواريخ والتحقق من التوفر
        form = BookingForm(request.POST, car_id=car.id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car

            booking.save() # السعر يحسب تلقائياً في الموديل
            messages.success(request, "تم حجز السيارة بنجاح! بانتظار الموافقة.")
            return redirect('bookings:booking_success')

            # ⬇ يروح إلى صفحة الدفع
            return redirect(reverse('payments:initiate_payment', args=[booking.id]))

    else:
        # ✅ نرسل car.id عند فتح الصفحة لأول مرة أيضاً
        form = BookingForm(car_id=car.id)

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'car': car
    })

# 2. صفحة نجاح الحجز (ستبقى للاستخدام إذا قررت عدم إلغائها)
@login_required
def booking_success(request):
    return render(request, 'bookings/booking_success.html')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def reviewer_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at')
    
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = get_object_or_404(Booking, id=booking_id)
        
        if action == 'approve':
            # 1. الموافقة على الحجز الحالي
            booking.status = 'CONFIRMED'
            booking.save()
            messages.success(request, f'Booking #{booking.id} Approved ✅')
            
            # 2. 🔥 إلغاء الحجوزات المتعارضة تلقائياً (Conflict Resolution)
            # نبحث عن أي حجوزات أخرى (Pending) لنفس السيارة تتقاطع مع تواريخ هذا الحجز
            conflicting_bookings = Booking.objects.filter(
                car=booking.car,
                status='PENDING',
                start_date__lte=booking.end_date,
                end_date__gte=booking.start_date
            ).exclude(id=booking.id)

            count = conflicting_bookings.count()
            if count > 0:
                conflicting_bookings.update(status='CANCELLED')
                messages.warning(request, f'⚠️ تم إلغاء {count} طلبات معلقة أخرى تلقائياً لمنع التعارض في التواريخ.')

        elif action == 'reject':
            booking.status = 'CANCELLED'
            booking.save()
            messages.warning(request, f'Booking #{booking.id} Rejected ❌')
        
        return redirect('bookings:reviewer_dashboard')


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