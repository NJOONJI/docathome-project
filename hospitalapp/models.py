from django.db import models

from adminapp.models import location, department, service
from guest.models import tbllogin, hospital,patient
from hospitalapp.models import *


# Create your models here.
class doctor(models.Model):
    docid = models.AutoField(primary_key=True)
    docname = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    qualification = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)
    depid = models.ForeignKey(department, on_delete=models.CASCADE, default="")
    hosid = models.ForeignKey(hospital, on_delete=models.CASCADE, default="")
    locid = models.ForeignKey(location, on_delete=models.CASCADE, default="")
    regdate = models.DateField(auto_now_add=True)
    loginid = models.ForeignKey(tbllogin, on_delete=models.CASCADE, default="")
    OnlineTime = models.TimeField()

class hosservice(models.Model):
    hosserid = models.AutoField(primary_key=True)
    serid = models.ForeignKey(service, on_delete=models.CASCADE, default="")
    hospitalid = models.ForeignKey(hospital, on_delete=models.CASCADE, default="")

class hospitaldepartment(models.Model):
    hosdepid = models.AutoField(primary_key=True)
    depid = models.ForeignKey(department, on_delete=models.CASCADE, default="")
    hosid = models.ForeignKey(hospital, on_delete=models.CASCADE, default="")

class complaint(models.Model):
    compid = models.AutoField(primary_key=True)
    patid = models.ForeignKey(patient, on_delete=models.CASCADE, default="")
    hosid = models.ForeignKey(hospital, on_delete=models.CASCADE, default="")
    compdetails = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True,null=True)

