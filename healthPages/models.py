from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Appointment(models.Model):
  fullname = models.CharField(max_length=100)
  mobileNo = models.IntegerField()
  email = models.EmailField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  appointmentDate = models.DateField("AppointmentDate Date(mm/dd/yyyy)",auto_now_add=False, auto_now=False, blank=True, null=True)
  area = models.CharField(max_length=250)
  district = models.CharField(max_length=100)
  description = models.CharField(max_length=500)