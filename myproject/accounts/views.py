from django.shortcuts import render, redirect
from .models import Patient
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':

        name = request.POST['name']
        age = request.POST['age']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        place = request.POST['city']
        password = request.POST['password']
        username = User.objects.filter(username=username)
        if username.exists():
            return HttpResponse("<script>alert('Already exist');window.location='/'</script>")
        else:
            user = User.objects.create_user(username=username, password=password)
            patient = Patient.objects.create(user=user, age=age, mobile=mobile, gender=gender, place=place, username=username,password=password)
            user.save()
            patient.save()
            return HttpResponse("<script>alert('Registered successfuly');window.location='/'</script>")
    return render(request,"register.html")

def login(request):
    if request.method == 'POST':
        
            username = request.POST('username')
            password = request.POST('password')
            user =authenticate(request,username=username,password=password)
            if user is not None:
                if user.groups.filter(name='Patient').exists():
                     login(request,user)
                     return redirect('login')
                else:
                     messages.error(request,'already exists')
        
            
            else:
                 messages.error(request,'invalid username or passsword')
         
        
    return render(request, 'login.html')

# def book_appointment(request):
#     if request.method == 'POST':
#             return redirect('')
#     appointments = Appointment.objects.all()
#     return render(request, 'booking.html')
