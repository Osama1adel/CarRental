from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from vehicles.models import Car 
from datetime import timedelta

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'قيد المراجعة'),
        ('CONFIRMED', 'مؤكد'),
        ('ACTIVE', 'قيد الاستخدام'),
        ('COMPLETED', 'مكتمل'),
        ('CANCELLED', 'ملغي'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="العميل"
    )
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="السيارة"
    )

    start_date = models.DateTimeField(verbose_name="تاريخ الاستلام")
    end_date = models.DateTimeField(verbose_name="تاريخ التسليم")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING',
        verbose_name="حالة الحجز"
    )
    
    # حقل لحساب الأيام
    duration_days = models.IntegerField(default=0, verbose_name="مدة الحجز بالأيام")
    
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="السعر الإجمالي"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"

    def __str__(self):
        return f"Booking #{self.id} - {self.user} - {self.car}"
    
    # دالة جديدة لحساب السعر والمدة
    def calculate_prices(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            
            # يجب استخدام .days + 1 لتضمين يومي الاستلام والتسليم
            
            self.duration_days = max(1, delta.days + 1)
        else:
            self.duration_days = 0

        if self.car and self.duration_days > 0:
            
            self.total_price = self.car.daily_price * self.duration_days
        else:
            self.total_price = 0.00


    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("تاريخ التسليم يجب أن يكون بعد تاريخ الاستلام.")
            
            if not self.pk and self.start_date < timezone.now():
                raise ValidationError("لا يمكن الحجز في تاريخ قديم.")

    def save(self, *args, **kwargs):
        
        self.calculate_prices()
        super().save(*args, **kwargs)