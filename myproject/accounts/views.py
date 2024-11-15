from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Appointment, Notification, Feedback, Prescription
from django.http import HttpResponse, JsonResponse,HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         logger.debug(f"POST data: {request.POST}")
#         patient_id = request.POST['patient']
#         doctor = request.POST['doctor']
#         case = request.POST['case']
#         date = request.POST['date']
#         time = request.POST['time']
        
#         patient = get_object_or_404(Patient, pk=patient_id)
#         logger.debug(f"Patient: {patient}")

#         if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
#             logger.debug(f"Time slot already booked: {doctor}, {date}, {time}")
#             return JsonResponse({'success': False, 'error': 'Time slot already booked'})
#         else:
#             appointment = Appointment(patient=patient, doctor=doctor, case=case, date=date, time=time)
#             appointment.save()
#             logger.debug(f"Appointment created: {appointment}")
#             return JsonResponse({'success': True, 'appointment_id': appointment.app_id})

#     return render(request, 'booking.html')
# views.py
# views.py
@login_required
def book_appointment(request):
    if request.method == 'POST':
        name = request.POST['patient']
        doctor = request.POST['doctor']
        case = request.POST['case']
        date = request.POST['date']
        time = request.POST['time']
        slot = request.POST['slot']  # Added slot field
        token = request.POST['token']

        patient = get_object_or_404(Patient, user=request.user)

        if Appointment.objects.filter(doctor=doctor, date=date, time=time, slot=slot, token=token).exists():
            return HttpResponse("<script>alert('Token already booked');window.location='/'</script>")

        appointment = Appointment(patient=patient, doctor=doctor, case=case, date=date, time=time, slot=slot, token=token)
        appointment.save()
        return HttpResponse("<script>alert('Appointment Booking Successfull');window.location='/'</script>")

    return render(request, 'booking.html')


def get_available_tokens(request):
    doctor = request.GET.get('doctor')
    date = request.GET.get('date')
    time = request.GET.get('time')
    slot = request.GET.get('slot')  # Added slot parameter
    
    booked_tokens = Appointment.objects.filter(doctor=doctor, date=date, time=time, slot=slot).values_list('token', flat=True)
    
    response_data = {'bookedTokens': list(map(int, booked_tokens))}
    return JsonResponse(response_data)



from datetime import timedelta
@login_required(login_url='/login/')
def appointment_history(request):
    patient = request.user.patient
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    appointments = Appointment.objects.filter(
        patient=patient
    ).exclude(
        status="Canceled", canceled_at__lt=twenty_four_hours_ago  # Exclude appointments canceled over 24 hours ago
    ).order_by('-date')
    return render(request, 'view.html', {'appointments': appointments})

from django.utils import timezone
def cancel_appointment(request, app_id):
    appointment = get_object_or_404(Appointment, app_id=app_id, patient=request.user.patient)
    if appointment.status != "Canceled":
        appointment.status = "Canceled"
        appointment.canceled_at = timezone.now()  # Set the cancellation time
        appointment.save()
        messages.success(request, "Your appointment has been canceled.")
    else:
        messages.info(request, "This appointment is already canceled.")
    return redirect('appointment')

# In your views.py file

from django.http import JsonResponse
from .models import Appointment

def check_doctor_availability(request):
    doctor = request.GET.get('doctor')
    date = request.GET.get('date')
    
    # Check if the doctor has an appointment on the selected date
    if doctor and date:
        appointments = Appointment.objects.filter(doctor=doctor, date=date)
        
        # If there are any appointments for the doctor on the selected date, return isBooked = True
        if appointments.exists():
            return JsonResponse({'isBooked': True})
        else:
            return JsonResponse({'isBooked': False})
    
    return JsonResponse({'isBooked': False})


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        place = request.POST['place']
        password = request.POST['password']
        username = request.POST['username']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("<script>alert('Username already exists');window.location='/'</script>")
        else:
            # Create the User
            user = User.objects.create_user(username=username, password=password)
            # Create the Patient without passing 'username'
            patient = Patient.objects.create(user=user,age=age, mobile=mobile, gender=gender, place=place)
            user.save()
            patient.save()
            return HttpResponse("<script>alert('Registered successfully');window.location='/'</script>")
    
    return render(request, "register.html")


@login_required(login_url='/login/')
def profile_update(request):
    patient = Patient.objects.get(user=request.user)  # Get the Patient instance linked to the logged-in user
    if request.method == 'POST':
        patient.age = request.POST['age']
        patient.mobile = request.POST['mobile']
        patient.gender = request.POST['gender']
        patient.place = request.POST['place']
        patient.save()
        return HttpResponse("<script>alert('Profile updated successfully');window.location='/'</script>")
    
    return render(request, "profile_update.html", {'patient': patient})

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        print(f"{username} {password}")
        if user is not None:
            print("Authentication successful")
            login(request, user)
            return redirect('home')  # Change to your intended redirect target
        else:
            print("Authentication failed")
            return HttpResponse("<script>alert('wrong password or username');window.location='/'</script>")

    return render(request, 'login.html')

import re

# Function to validate password strength
def validate_password(password):
    # Check length (at least 8 characters)
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # Check if the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."

    # Check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."

    # Check if the password contains at least one digit
    if not re.search(r'[0-9]', password):
        return "Password must contain at least one digit."

    # Check if the password contains at least one special character
    if not re.search(r'[@#$%^&+=]', password):
        return "Password must contain at least one special character."

    return None  # No validation errors

# View to handle direct password reset
def direct_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if both passwords match
        if new_password1 != new_password2:
            return render(request, 'password.html', {'error': 'Passwords do not match'})

        # Validate the new password
        password_error = validate_password(new_password1)
        if password_error:
            return render(request, 'password.html', {'error': password_error})

        # Attempt to retrieve the user by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'password.html', {'error': 'Username does not exist'})

        # Update the password if user exists
        user.password = make_password(new_password1)  # Hash the new password
        user.save()
        return HttpResponse("<script>alert('Password reset successful!');window.location='/login/';</script>")

    return render(request, 'password.html')



def custom_logout_view(request):
    logout(request)
    return redirect(reverse('home'))
def home_page(request):
    return render(request, 'home.html')
def about_us(request):
    return render(request, 'about.html')

# def doctor_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(request, username=username, password=password)
#         print(f"{username} {password}")
#         if user is not None:
#             print("Authentication successful")
#             login(request, user)
#             return redirect('/')  # Change to your intended redirect target
#         else:
#             print("Authentication failed")
#             return HttpResponse("<script>alert('wrong password or username');window.location='/'</script>")

#     return render(request, 'patient_login.html')

# def user(request):
#     return render(request,'user.html')

@login_required(login_url='/login/')
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})

def mark_as_read(request, id):
    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_notifications')



# views.py


@login_required(login_url='/login/')
def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            feedback = Feedback(user=request.user, message=message)
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            logger.info(f"Feedback submitted: {feedback.message} by {request.user.username}")
            return redirect('home')  # Redirect to a success page or another view
        else:
            messages.error(request, "Please enter a feedback message.")
    return render(request, 'feedback.html')

@login_required(login_url='/login/')

def view_prescription(request):
    if request.user.is_authenticated:
        try:
            # Get the Patient instance for the logged-in user
            patient = Patient.objects.get(user=request.user)
            # Filter prescriptions linked to this patient
            prescriptions = Prescription.objects.filter(patient=patient)
            return render(request, 'precription.html', {'prescriptions': prescriptions})
        except Patient.DoesNotExist:
            return HttpResponse("<script>alert('No prescription found.');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Please login to view prescriptions');window.location='/'</script>")



