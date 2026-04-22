from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clinic, Doctor, Appointment
from .forms import RegisterForm, AppointmentForm
from django.utils.translation import gettext_lazy as _

def home(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinic/home.html', {'clinics': clinics})

def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinic/clinic_list.html', {'clinics': clinics})

def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = Doctor.objects.filter(clinic=clinic)
    return render(request, 'clinic/clinic_detail.html', {'clinic': clinic, 'doctors': doctors})

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.doctor = doctor
            appointment.save()
            messages.success(request, _('Appointment booked successfully.'))
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'clinic/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'clinic/dashboard.html', {'appointments': appointments})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'clinic/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, _('Invalid credentials.'))
    return render(request, 'clinic/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')
