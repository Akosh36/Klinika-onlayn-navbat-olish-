from django.contrib import admin
from .models import Clinic, Doctor, Appointment

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'clinic')
    list_filter = ('clinic', 'specialty')
    search_fields = ('name', 'specialty')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor__clinic')
    search_fields = ('user__username', 'doctor__name')
