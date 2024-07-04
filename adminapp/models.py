from datetime import date

from django.db import models


# Create your models here.
class district(models.Model):
    disid = models.AutoField(primary_key=True)
    disname = models.CharField(max_length=50)

class location(models.Model):
    locid = models.AutoField(primary_key=True)
    locname = models.CharField(max_length=50)
    disid = models.ForeignKey(district, on_delete=models.CASCADE, default="")

class department(models.Model):
    depid = models.AutoField(primary_key=True)
    depname = models.CharField(max_length=50)
    depphoto = models.ImageField()

class service(models.Model):
    serid = models.AutoField(primary_key=True)
    sername = models.CharField(max_length=50)
    serTime = models.IntegerField(null=True)
    serphoto = models.ImageField(null=True)





from django.db import models

# Create your models here.
