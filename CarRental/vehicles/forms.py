from django import forms
from .models import Car, RentalCompany, CarReview

class RentalCompanyForm(forms.ModelForm):
    class Meta:
        model = RentalCompany
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: شركة سريعة للتأجير'}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['rental_company', 'brand', 'model_name', 'description', 'daily_price', 
                  'transmission', 'fuel_type', 'color', 'plate_number', 
                  'image', 'is_available']
        
        # تنسيق الحقول ب Bootstrap
        widgets = {
            'rental_company': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: تويوتا'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: كامري'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'plate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, str(i)) for i in range(1, 6)], # خيارات من 1 إلى 5
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'أضف تعليقك هنا...'}),
        }