# Clinic Appointment System

A professional, multi-language Django web application for booking medical appointments with a modern, responsive design.

## Features

- **Multi-language Support**: English, Russian, Uzbek
- **User Authentication**: Registration and login with secure forms
- **Clinic & Doctor Management**: Browse clinics and view doctors
- **Appointment Booking**: Easy booking with date/time selection
- **User Dashboard**: Manage personal appointments
- **Admin Panel**: Full Django admin integration for data management
- **Responsive Design**: Bootstrap 5 with custom styling and FontAwesome icons
- **Professional UI**: Modern gradients, hover effects, and clean layout

## Screenshots

- Hero section with call-to-action
- Card-based clinic and doctor listings
- Centered forms with icons
- Status badges in dashboard
- Responsive navbar with language switcher

## Technical Stack

- **Backend**: Django 6.0.4
- **Database**: SQLite
- **Frontend**: Bootstrap 5, FontAwesome, Custom CSS
- **Internationalization**: Django i18n with gettext

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Create superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

4. Run the server:
   ```
   python manage.py runserver
   ```

5. Access the application at http://127.0.0.1:8000/

## Sample Data

The application includes sample clinics and doctors. To add more:

```python
from clinic.models import Clinic, Doctor

clinic = Clinic.objects.create(
    name="Your Clinic Name",
    address="Address",
    description="Description"
)
Doctor.objects.create(
    name="Dr. Name",
    specialty="Specialty",
    clinic=clinic
)
```

## Admin Panel

Access `/admin/` to manage clinics, doctors, and appointments.

## Languages

Switch languages using the globe icon in the navbar.

## Customization

- Styles: `clinic/static/clinic/css/style.css`
- Templates: `clinic/templates/clinic/`
- Colors: Blue gradient theme with medical icons

## Production Deployment

For production, configure:
- Environment variables for secrets
- PostgreSQL database
- Static files serving
- HTTPS
- Email notifications (optional)