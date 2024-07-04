import smtplib
from email.message import EmailMessage

from django.db.models import Max
from django.shortcuts import render, redirect
from guest.models import *
from django.http import HttpResponse, JsonResponse
import random
import string

from hospitalapp.models import doctor


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if tbllogin.objects.filter(email=email, password=password).exists():
            loginobj = tbllogin.objects.get(email=email, password=password)
            request.session['email'] = loginobj.email
            request.session['loginid'] = loginobj.loginid
            role = loginobj.role
            if role == 'admin':
                return redirect('/admin/index')
            elif role=='hospital':
                if loginobj.status=="accepted":
                    return redirect('/hospital/home')
                else:
                    return HttpResponse(
                        "<script>alert('Not verified yet');window.location='guest/login.html';</script>")
                    return redirect('/guest/login')
            elif role == 'doctor' :
                return redirect('/hospital/home')
            elif role == 'patient':
                return redirect('/patient/home')
            else:
                return HttpResponse(
                    "<script>alert('Not an authorized person');window.location='/guest/login/';</script>")
                #return render(request, 'guest/login.html')
        else:
            return HttpResponse(
                "<script>alert('Invalid username or password');window.location='/guest/login/';</script>")
    else:
        return render(request, 'guest/login.html')


def index(request):
    return render(request,"guest/index.html")
def hospitalreg(request):
        if request.method == 'POST':
            lob=tbllogin()
            lob.email=request.POST.get('email')
            lob.password = request.POST.get('password')
            lob.role='hospital'
            lob.status = 'requested'
            if tbllogin.objects.filter(email=request.POST.get('email'),password=request.POST.get('password')).exists():
                    return HttpResponse("<script>alert('Duplicate..');window.location='/guest/hospitalreg';</script>")
            lob.save()
            hosname = request.POST.get('hosname')
            phone = request.POST.get('phone')
            if hospital.objects.filter(hosname=hosname).exists():
                    return HttpResponse("<script>alert('Duplicate..');window.location='/guest/hospitalreg';</script>")
            hosobj = hospital()
            hosobj.hosname = hosname
            hosobj.phone = phone
            hosobj.locid = location.objects.get(locid=request.POST.get('locname'))
            hosobj.licencephoto = request.FILES['licencephoto']
            hosobj.hosphoto = request.FILES['hosphoto']
            hosobj.loginid=lob
            hosobj.save()
            return HttpResponse("<script>alert('Successfully Registered');window.location='/guest/hospitalreg';</script>")
        else:
            dis = district.objects.all()
            return render(request, "guest/hospitalreg.html",{'dis':dis})


def filllocation(request):
    did=(request.POST.get("did"))
    loc=location.objects.filter(disid =did).values()
    return JsonResponse(list(loc),safe=False)
def patientreg(request):
    if request.method == 'POST':
        lob = tbllogin()
        lob.email = request.POST.get('email')
        lob.password = request.POST.get('password')
        lob.role = 'patient'
        lob.status = 'confirmed'
        if tbllogin.objects.filter(email=request.POST.get('email')).exists():
            return HttpResponse("<script>alert('Already Exists..');window.location='/guest/patientreg';</script>")
        else:
            lob.save()
            patname = request.POST.get('patname')
            phone = request.POST.get('phone')
            patobj = patient()
            patobj.patname = patname
            patobj.gender = request.POST.get('gender')
            patobj.age = request.POST.get('age')
            patobj.housename = request.POST.get('housename')
            patobj.pin = request.POST.get('pin')
            opno = patient.objects.aggregate(max_value=Max('opno'))['max_value']
            if opno is not None:
                opnonew=int(opno)+1
            else:
                opnonew=1
            patobj.opno=opnonew

            patobj.email = request.POST.get('email')
            patobj.phone = phone
            patobj.locid = location.objects.get(locid=request.POST.get('locname'))
            patobj.loginid = lob
            patobj.save()
            patobj.save()


            return HttpResponse(
                "<script>alert('Successfully Registerd');window.location='/guest/patientreg';</script>")

    else:
        dis = district.objects.all()
        return render(request, "guest/patientreg.html", {'dis': dis})


def filllocation(request):
    did = (request.POST.get("did"))
    loc = location.objects.filter(disid=did).values()
    return JsonResponse(list(loc), safe=False)


def forgotpassword(request):
    if request.method == 'POST':
        uname = request.POST.get("email")
        if tbllogin.objects.filter(email=uname).exists():
            lg = tbllogin.objects.get(email=uname)
            lid = lg.loginid
            if lg.role == "doctor":
                details = doctor.objects.get(loginid_id=lid)
                customer_name=details.docname
            elif lg.role == "hospital":
                details= hospital.objects.get(loginid_id=lid)
                customer_name = details.hosname
            else:
                details= patient.objects.get(loginid_id=lid)
                customer_name = details.patname
            email = lg.email

            characters = string.ascii_letters + string.digits
            random_number = ''.join(random.choice(characters) for _ in range(8))
            # return HttpResponse(random_number)
            lg.password = random_number
            lg.save()
            msg = EmailMessage()
            msg.set_content(f'Hi {customer_name},Your new password to login in is {random_number}')
            msg['Subject'] = "Forgot Password ?"
            msg['from'] = 'albybennichen15@gmail.com'
            msg['To'] = {email}
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('albybennichen15@gmail.com', 'hqmo pbhe uyhl yvxm')
                smtp.send_message(msg)
                return HttpResponse("<script>alert('Login with new password in your email');window.location='/guest/login';</script>")
        return HttpResponse("<script>alert('No datafound');window.location=' /guest/forgotpassword';</script>")
    return render(request, "guest/forgotpassword.html")

# Create your views here.
