# payments/models.py
from django.db import models
from bookings.models import Booking # استيراد نموذج الحجز

class RentalPayment(models.Model):
    STATUS_CHOICES = [
        ('INITIATED', 'تم البدء'),
        ('PENDING_PAYLINK', 'قيد انتظار Paylink'),
        ('COMPLETED', 'اكتمل بنجاح'),
        ('FAILED', 'فشل'),
    ]

    # ربط عملية الدفع بسجل الحجز
    rental_booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='payment',
        verbose_name="الحجز المرتبط"
    )
    # لحفظ رقم العملية الذي يُصدره Paylink
    transaction_id = models.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="رقم عملية Paylink"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='INITIATED',
        verbose_name="حالة الدفع"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.rental_booking.id} - {self.status}"