from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from bookings.models import Booking
from .models import RentalPayment
from .paylink_service import create_paylink_invoice 


def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if hasattr(booking, 'payment') and booking.payment.status == 'COMPLETED':
        return redirect(reverse('payments:payment_success', args=[booking.id]))

    # رابط العودة بعد الدفع
    callback_url = request.build_absolute_uri(reverse('payments:paylink_callback'))

    try:

        invoice_info = create_paylink_invoice(booking=booking, callback_url=callback_url)
    except Exception as e:
        # logger.error(f"Paylink Invoice Creation Failed for Booking #{booking_id}: {e}")
        return redirect('payments:payment_failed') 
    
    payment, created = RentalPayment.objects.update_or_create(
        rental_booking=booking,
        defaults={
            'transaction_id': invoice_info['transaction_no'],
            'amount': booking.total_price,
            'status': 'PENDING_PAYLINK'
        }
    ) #

    return redirect(invoice_info['payment_url']) 

# def paylink_callback(request):
#     # Paylink يرسل البيانات عبر GET بعد إتمام الدفع (في وضع الاختبار)
#     transaction_no = request.GET.get('TransactionNo')
#     order_number = request.GET.get('OrderNumber') # هو ID الحجز

#     if not transaction_no or not order_number:
#         return redirect('payments:payment_failed') #

#     try:
#         # invoice_details = paylink.get_invoice(transaction_no=transaction_no)
        
#         local_payment = RentalPayment.objects.get(transaction_id=transaction_no)
#         booking = local_payment.rental_booking
        
#         if invoice_details.transactionStatus == 'COMPLETED':
#             local_payment.status = 'COMPLETED'
#             local_payment.save()
#             booking.status = 'PENDING'
#             booking.save()

#             return redirect(reverse('payments:payment_success', args=[booking.id]))

#         else:
#             local_payment.status = 'FAILED'
#             local_payment.save()
#             return redirect('payments:payment_failed')
            
#     except Exception as e:
#         logger.error(f"Paylink Callback Failed: {e}") 
#         return redirect('payments:payment_failed')



# Success Page :
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payments/success.html', {'booking': booking})

# Faild Page :
@login_required
def payment_failed(request):
    return render(request, 'payments/failed.html')