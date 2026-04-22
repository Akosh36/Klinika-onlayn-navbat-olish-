from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Clinic(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    address = models.TextField(_('Address'))
    description = models.TextField(_('Description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Clinic')
        verbose_name_plural = _('Clinics')

class Doctor(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    specialty = models.CharField(_('Specialty'), max_length=100)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name=_('Clinic'))

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    class Meta:
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name=_('Doctor'))
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'))
    status = models.CharField(_('Status'), max_length=20, choices=[
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name} on {self.date} at {self.time}"

    class Meta:
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')
