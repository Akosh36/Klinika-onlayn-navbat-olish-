"""URL configuration for clinic_appointment project."""
from django.contrib import admin
from django.urls import path, include

from clinic.views_i18n import change_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uz/', include('clinic.urls')),
    path('ru/', include('clinic.urls')),
    path('', include('clinic.urls')),
    path('change-language/', change_language, name='change_language'),
]
