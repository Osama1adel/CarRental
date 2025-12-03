# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .paylink_service import create_paylink_invoice, paylink
from .models import RentalPayment
from bookings.models import Booking

# أ. دالة بدء الدفع (تستقبل ID الحجز)
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # التحقق: إذا كان الحجز مدفوعاً بالفعل
    if hasattr(booking, 'payment') and booking.payment.status == 'COMPLETED':
        return redirect(reverse('payments:payment_success', args=[booking.id]))

    # رابط العودة بعد الدفع
    callback_url = request.build_absolute_uri(reverse('payments:paylink_callback'))

    try:
        invoice_info = create_paylink_invoice(booking=booking, callback_url=callback_url)
    except Exception:
        # يمكن إضافة رسالة فشل مناسبة
        return redirect('payments:payment_failed')
    
    # إنشاء/تحديث سجل الدفع المحلي
    payment, created = RentalPayment.objects.update_or_create(
        rental_booking=booking,
        defaults={
            'transaction_id': invoice_info['transaction_no'],
            'amount': booking.total_price,
            'status': 'PENDING_PAYLINK'
        }
    )

    # التوجيه إلى Paylink
    return redirect(invoice_info['payment_url'])

# ب. دالة التحقق من الدفع (الـ Callback)
def paylink_callback(request):
    transaction_no = request.GET.get('TransactionNo')
    order_number = request.GET.get('OrderNumber') # هو ID الحجز

    if not transaction_no or not order_number:
        return redirect('payments:payment_failed')

    try:
        invoice_details = paylink.get_invoice(transaction_no=transaction_no)
        local_payment = RentalPayment.objects.get(transaction_id=transaction_no)
        booking = local_payment.rental_booking

        # التحقق الأمني: الحالة والمبلغ
        paylink_status = invoice_details.order_status.lower()
        amount_paid = float(invoice_details.amount)
        expected_amount = float(booking.total_price)

        if paylink_status == 'paid' and amount_paid == expected_amount:
            # النجاح! تحديث الحالة
            local_payment.status = 'COMPLETED'
            local_payment.save()
            booking.status = 'CONFIRMED' # أو حالة تعبر عن الدفع
            booking.save()
            return redirect(reverse('payments:payment_success', args=[booking.id]))
        else:
            # فشل
            local_payment.status = 'FAILED'
            local_payment.save()
            return redirect('payments:payment_failed')

    except Exception:
        return redirect('payments:payment_failed')

# ج. دالة نجاح/فشل
def payment_success(request, booking_id):
    # يمكن هنا عرض رسالة تأكيد للعميل
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payments/success.html', {'booking': booking})

def payment_failed(request):
    return render(request, 'payments/failed.html')