from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clinics/', views.clinic_list, name='clinic_list'),
    path('clinics/<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('set-language/<str:language>/', views.set_language, name='set_language'),
]