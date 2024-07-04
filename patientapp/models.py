from django.db import models

from adminapp.models import location, department, service
from guest.models import tbllogin, patient,hospital
from hospitalapp.models import hosservice, doctor

from patientapp.models import *


class appointment(models.Model):
    appid = models.AutoField(primary_key=True)
    patid = models.ForeignKey(patient, on_delete=models.CASCADE, default="")
    hosserid = models.ForeignKey(hosservice, on_delete=models.CASCADE, default="")
    reqdate = models.DateField(auto_now_add=True,null=True)
    appdate = models.DateField(null=True)
    apptime = models.TimeField(null=True)
    status = models.CharField(max_length=50)
    docid = models.ForeignKey(doctor, on_delete=models.CASCADE, null=True)
    remark = models.CharField(max_length=300,null=True)

class patienthistory(models.Model):
    caseid = models.AutoField(primary_key=True)
    appid =models.ForeignKey(appointment, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=50)
    symptoms = models.CharField(max_length=50)
    prescription = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True,null=True)

class feedback(models.Model):
    feedid = models.AutoField(primary_key=True)
    patid = models.ForeignKey(patient, on_delete=models.CASCADE, default="")
    hosid = models.ForeignKey(hospital, on_delete=models.CASCADE, default="")
    feeddetails = models.CharField(max_length=50)



# Create your models here.
