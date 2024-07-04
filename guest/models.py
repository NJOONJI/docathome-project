from django.db import models
from adminapp.models import *
class tbllogin(models.Model):
    loginid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

class hospital(models.Model):
    hosid = models.AutoField(primary_key=True)
    hosname = models.CharField(max_length=50)
    locid = models.ForeignKey(location, on_delete=models.CASCADE, default="")
    regdate = models.DateField(default=date.today)
    licencephoto = models.ImageField()
    phone = models.CharField(max_length=50)
    loginid = models.ForeignKey(tbllogin, on_delete=models.CASCADE, default="")
    hosphoto = models.ImageField(null=True)

class patient(models.Model):
    patid = models.AutoField(primary_key=True)
    patname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    locid = models.ForeignKey(location, on_delete=models.CASCADE, default="")
    gender = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    housename = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    regdate = models.DateField(auto_now_add=True)
    opno = models.CharField(max_length=50)
    loginid = models.ForeignKey(tbllogin, on_delete=models.CASCADE, default="")