"""
URL configuration for CarRental project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # هذا الرابط الأساسي لتطبيق السيارات
    path('cars/', include('vehicles.urls')), 
    
    path("accounts/", include("accounts.urls")),
    path("", include("main.urls")),
    path("booking/", include("bookings.urls")),
    path('payments/', include('payments.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)