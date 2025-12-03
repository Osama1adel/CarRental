# accounts/forms.py
from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

# 1. Form for updating basic User data (Name, Email)
class UserUpdateForm(forms.ModelForm):
    # Keep email read-only since it's used as the username for login
    email = forms.EmailField(disabled=True) 
    
    class Meta:
        model = User
        fields = ['first_name', 'email'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        labels = {
            'first_name': 'Full Name',
            'email': 'Email Address (Read-only)',
        }

# 2. Form for updating UserProfile data (Phone, DOB, Documents)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'national_id_image', 'driving_license_image']
        labels = {
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'national_id_image': 'National ID / Residency Image',
            'driving_license_image': 'Driving License Image',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Example: 05xxxxxxxx'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'national_id_image': forms.FileInput(attrs={'class': 'form-control'}),
            'driving_license_image': forms.FileInput(attrs={'class': 'form-control'}),
        }