# Generated by Django 4.1 on 2024-05-01 05:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbllogin',
            fields=[
                ('loginid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('patid', models.AutoField(primary_key=True, serialize=False)),
                ('patname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.BigIntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=50)),
                ('housename', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50)),
                ('regdate', models.DateField(auto_now_add=True)),
                ('opno', models.CharField(max_length=50)),
                ('locid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminapp.location')),
                ('loginid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='guest.tbllogin')),
            ],
        ),
        migrations.CreateModel(
            name='hospital',
            fields=[
                ('hosid', models.AutoField(primary_key=True, serialize=False)),
                ('hosname', models.CharField(max_length=50)),
                ('regdate', models.DateField(default=datetime.date.today)),
                ('licencephoto', models.ImageField(upload_to='')),
                ('phone', models.CharField(max_length=50)),
                ('hosphoto', models.ImageField(null=True, upload_to='')),
                ('locid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminapp.location')),
                ('loginid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='guest.tbllogin')),
            ],
        ),
    ]
