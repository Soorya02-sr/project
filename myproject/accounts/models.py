from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    GENDER_CHOICES = [
        ('',''),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    patient_id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    place = models.CharField(max_length=100)
    
    def _str_(self):
        return self.user.username
    

    
# models.py
# models.py
class Appointment(models.Model):
    app_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.CharField(max_length=20)
    doctor = models.CharField(max_length=20)
    date = models.DateField()
    time = models.CharField(max_length=10, choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')])
    slot = models.CharField(max_length=10)  # New field for time slot
    token = models.CharField(max_length=50)
    STATUS_CHOICES = [("Active", "Active"), ("Canceled", "Canceled")]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")
    canceled_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        unique_together = ('doctor', 'date', 'time', 'slot', 'token')

    def _str_(self):
        return f"Appointemnt {self.app_id}"

    
class Doctor(models.Model):
    doc_id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile=models.ImageField(upload_to='media/doctor/',null=True,blank=False)
    doc_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    phone=models.IntegerField()
    special=models.CharField(max_length=50)
    Dept=models.CharField( max_length=50)
    quali=models.CharField( max_length=50)
    exp=models.CharField(max_length=20)
    status=models.BooleanField(default=False)
    def _str_(self):
        return self.user.username

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"




class Feedback(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)  # To mark if the feedback is reviewed by admin

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class Prescription(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)  # Link to the Patient model
    diagnosis = models.TextField()
    chief_complaint = models.TextField()
    
    # Treatment plan represented by selections for each quadrant
    quadrant_1_tooth = models.IntegerField(choices=[(i, str(i)) for i in range(1, 9)], blank=True, null=True)
    quadrant_2_tooth = models.IntegerField(choices=[(i, str(i)) for i in range(1, 8)], blank=True, null=True)
    quadrant_3_tooth = models.IntegerField(choices=[(i, str(i)) for i in range(1, 8)], blank=True, null=True)
    quadrant_4_tooth = models.IntegerField(choices=[(i, str(i)) for i in range(1, 8)], blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.user.username}"




