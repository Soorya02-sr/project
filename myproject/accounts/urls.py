from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
      path('',views.home_page,name="home"),
      path('register/',views.register,name="register"),
      path('profile_update/', views.profile_update, name='profile_update'),
      path('password_reset/', views.direct_password_reset, name='password_reset'),
      path('login/',views.patient_login,name="login"),
      path('logout/',views.custom_logout_view, name='logout'),
      path('home/', views.home_page, name='home_page'),
      path('aboutus/', views.about_us, name='about_us'),
      path('appointment/',views.book_appointment,name="appointment"),
      path('get_available_tokens/', views.get_available_tokens, name="get_available_tokens"),
      path('appointment-history/', views.appointment_history, name='appointment_history'),
      path('cancel-appointment/<int:app_id>/', views.cancel_appointment, name='cancel_appointment'),
      
      path('notification/', views.user_notifications, name='user_notifications'),
      path('notifications/read/<int:id>/', views.mark_as_read, name='mark_as_read'),
      path('prescriptions/', views.view_prescription, name='view_prescription'),

      path('check_doctor_availability/', views.check_doctor_availability, name='check_doctor_availability'),

      path('feedback/', views.submit_feedback, name='submit_feedback'),


      
]
