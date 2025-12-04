from django import forms
from .models import Booking
from django.db.models import Q

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    # نستقبل رقم السيارة (car_id) عند إنشاء الفورم لنعرف أي سيارة نفحص
    def __init__(self, *args, **kwargs):
        self.car_id = kwargs.pop('car_id', None) 
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        # 1. التحقق من منطقية التواريخ (النهاية بعد البداية)
        if start and end and end <= start:
            raise forms.ValidationError("تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")

        # 2. التحقق من توفر السيارة (منع التداخل مع حجوزات مؤكدة)
        if self.car_id and start and end:
            # نبحث عن أي حجز 'CONFIRMED' لنفس السيارة يتقاطع مع الفترة المختارة
            overlap = Booking.objects.filter(
                car_id=self.car_id,
                status='CONFIRMED'
            ).filter(
                start_date__lt=end,  # يبدأ قبل أن ينتهي حجزنا
                end_date__gt=start   # وينتهي بعد أن يبدأ حجزنا
            ).exists()

            if overlap:
                # هذا الخطأ هو الذي سيظهر في المستطيل الأحمر في ملف HTML
                raise forms.ValidationError("عذراً، السيارة محجوزة بالفعل ومؤكدة في هذه الفترة. يرجى اختيار تواريخ أخرى.")
        
        return cleaned_data