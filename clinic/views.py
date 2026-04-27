from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clinic, Doctor, Appointment
from .forms import RegisterForm, AppointmentForm
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.views.decorators.http import require_http_methods

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

@require_http_methods(["GET"])
def set_language(request, language):
    """Set the user's language preference"""
    from django.conf import settings
    
    # Validate language code
    valid_languages = [lang[0] for lang in settings.LANGUAGES]
    if language not in valid_languages:
        language = settings.LANGUAGE_CODE
    
    # Set language in session
    request.session['language'] = language
    translation.activate(language)
    
    # Get the referer or default to home
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the new language URL
    # Extract path from referer
    from urllib.parse import urlparse
    parsed = urlparse(referer)
    path = parsed.path
    
    # Remove language prefix from path if present
    for lang in valid_languages:
        if path.startswith(f'/{lang}/'):
            path = path[len(f'/{lang}'):]
            break
    
    # Ensure path is not empty
    if not path or path == '':
        path = '/'
    
    # Redirect to same path with new language prefix
    return redirect(f'/{language}{path}')

