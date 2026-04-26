"""URL configuration for clinic_appointment project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uz/', include('clinic.urls')),
    path('ru/', include('clinic.urls')),
    path('', include('clinic.urls')),
]
