from django.db import models

# Create your models here.

# accounts/models.py
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="User"
    )
    
    # New field: Phone Number
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name="Phone Number",
        validators=[
            RegexValidator(
                # A simple regex for common international numbers
                regex=r'^\+?1?\d{9,15}$', 
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )

    # New field: Date of Birth
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth"
    )
    
    # National ID or equivalent identification document
    national_id_image = models.ImageField(
        upload_to='documents/national_id/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="National ID Image"
    )
    
    # Driving License image
    driving_license_image = models.ImageField(
        upload_to='documents/driving_license/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name="Driving License Image"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    @property
    def has_required_documents(self):
        # Checks if both documents are uploaded
        return self.national_id_image and self.driving_license_image