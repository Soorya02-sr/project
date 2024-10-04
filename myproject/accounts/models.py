from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,default=1 )
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    place = models.CharField(max_length=100)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=8)  # Password hashing is recommended
    
    
    def _str_(self):
        return self.name
    def get_id(self):
        return self.user.id
    

# class Doctor(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile=models.ImageField(upload_to='media/doctor/',null=True,blank=False)
#     doc_name=models.CharField(max_length=20)
#     email=models.EmailField(max_length=20)
#     phone=models.IntegerField()
#     special=models.CharField(max_length=20)
#     Dept=models.CharField( max_length=50)
#     exp=models.CharField(max_length=20)
#     status=models.BooleanField(default=False)
#     def _str_(self):
#         return f'Dr. {self.doc_name}  ({self.special})'
#     def get_id(self):
#         return self.user.id
    
# class Appointment(models.Model):
#     cases = [
#         ('C', 'Cleaning'),
#         ('O', 'Orthodontics'),
#         ('R', 'Root Canal'),
#         ('I', 'Implant'),
#     ]
#     doctors= [
#         ('J', 'John Doe'),
#         ('P', 'Praveena Raj'),
#         ('R', 'Rahman'),
#         ('S', 'Saniya'),
#     ]
#     user=models.OneToOneField(User,on_delete=models.CASCADE,default=1)
#     name=models.CharField(max_length=20)
#     case = models.CharField(max_length=1, choices=cases)
#     doctor=models.CharField(max_length=1,choices= doctors, null=True)
#     date = models.DateField()
#     time = models.TimeField()
    
#     def __str__(self):
#         return f"{self.case} - {self.patient} "
#     def get_id(self):
#         return self.user.id