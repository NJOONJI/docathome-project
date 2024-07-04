import smtplib
from email.message import EmailMessage

from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from hospitalapp.models import hosservice,complaint
from patientapp.models import *
from adminapp.models import *
from guest.models import *
from django.http import HttpResponse, JsonResponse

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        return render(request, "patient/index.html" )
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def servicebooking(request):
    if "loginid" in request.session:
        hospital1=hospital.objects.all()
        dist=district.objects.all()
        return render(request,'patient/servicebooking.html',{'hospital':hospital1,'dist':dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

def filllocation(request):
    did = (request.POST.get("did"))
    loc = location.objects.filter(disid=did).values()
    return JsonResponse(list(loc), safe=False)

def fillservices(request):
    did = int(request.POST.get("did"))
    ser = hosservice.objects.filter(hospitalid_id=did).values('serid__serid','serid__sername')
    return JsonResponse(list(ser), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hosserviceview(request,id):
    if "loginid" in request.session:
        #return HttpResponse(id)
        services = hosservice.objects.filter(hospitalid__hosid=id)
        today_date = date.today()
        #return HttpResponse(services)
        return render(request, 'patient/service.html', {'today_date': today_date,'services': services,'hosid':id})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def servicerequest(request,id):
    if "loginid" in request.session:
        aob=appointment()
        aob.appdate=request.POST.get('requireddate')
        aob.apptime=request.POST.get('requiredtime')
        aob.hosserid = hosservice.objects.get(hosserid=request.POST.get('hosserid'))
        aob.patid=patient.objects.get(loginid_id=request.session['loginid'])
        aob.status="Requested"
        if appointment.objects.filter(patid=patient.objects.get(loginid_id=request.session['loginid']),appdate=request.POST.get('requireddate')).exists():
            #return HttpResponse("hai")
            return HttpResponse("<script>alert('Service Already Requested for "+aob.appdate+"');window.location='/patient/hosservice/" + id + "';</script>")
        else:
            #return HttpResponse("hello")
            aob.save()
            return HttpResponse("<script>alert('Successfully Requested:');window.location='/patient/hosservice/"+id+"';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bookingconfirmation(request):
    if "loginid" in request.session:
        details=appointment.objects.filter(patid=patient.objects.get(loginid_id=request.session['loginid']),status='Assigned')
        rdetails = appointment.objects.filter(patid=patient.objects.get(loginid_id=request.session['loginid']),
                                             status='Rejected')
        return render(request, 'patient/bookingconfirmation.html', {'rdetails':rdetails,'details':details,'bookingconfirmation': bookingconfirmation})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewmoreconfirmation(request,id):
    if "loginid" in request.session:
        details = appointment.objects.get(appid=id)
        return render(request, 'patient/viewmoreconfirmation.html', {'details': details})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewmorerejection(request,id):
    if "loginid" in request.session:
        details = appointment.objects.get(appid=id)
        return render(request, 'patient/viewmorerejection.html', {'details': details})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcasehistory(request):
    if "loginid" in request.session:
        details=patienthistory.objects.select_related('appid').filter(appid__status="Completed",appid__patid=patient.objects.get(loginid__loginid=request.session['loginid'])).values('appid__hosserid__serid__sername','appid__appdate','appid__apptime','description','symptoms','prescription')
        return render(request, 'patient/viewcasehistory.html',{'details': details})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

def fillhospital(request):
    did = int(request.POST.get("did"))
    ser = hospital.objects.filter(locid=did).values()
    return JsonResponse(list(ser), safe=False)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def complaintreg(request):
    if "loginid" in request.session:
        hospital1 = hospital.objects.all()
        dist = district.objects.all()
        return render(request, 'patient/complaintreg.html', {'hospital': hospital1, 'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def complaintnew(request,id):
    if "loginid" in request.session:
        if request.method == 'POST':
            comdetails = request.POST.get('compdetails')
            obj=complaint()
            obj.compdetails = comdetails
            obj.hosid=hospital.objects.get(hosid=id)
            obj.patid=patient.objects.get(loginid__loginid=request.session['loginid'])
            obj.save()
            return HttpResponse(
                "<script>alert('Complaint Successfully Registered');window.location='/patient/complaintreg';</script>")
        comp=complaint.objects.filter()
        return render(request, "patient/complaintnew.html",{'hid':id,'complaint':comp})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecomplaint(request, id):
    if "loginid" in request.session:
        comp = complaint.objects.get(compid=id)
        comp.delete()
        return HttpResponse(
            "<script>alert('Complaint Successfully Deleted');window.location='/patient/complaintview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedbackreg(request):
    if "loginid" in request.session:
        hospital1 = hospital.objects.all()
        dist = district.objects.all()
        return render(request, 'patient/feedbackreg.html', {'hospital': hospital1, 'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedbacknew(request,id):
    if "loginid" in request.session:
        if request.method == 'POST':
            feedetails = request.POST.get('feeddetails')
            obj=feedback()
            obj.feeddetails = feedetails
            obj.hosid=hospital.objects.get(hosid=id)
            obj.patid=patient.objects.get(loginid__loginid=request.session['loginid'])
            obj.save()
            return HttpResponse(
                "<script>alert('Complaint Successfully Registered');window.location='/patient/feedbackreg';</script>")
        feed=feedback.objects.filter()
        return render(request, "patient/feedbacknew.html",{'hid':id,'feedback':feed})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletefeedback(request, id):
    if "loginid" in request.session:
        feed = feedback.objects.get(feedid=id)
        feed.delete()
        return HttpResponse(
            "<script>alert('Complaint Successfully Deleted');window.location='/patient/feedbackreg';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")
def changepassword(request):

    if request.method == 'POST':
        uname = request.POST.get("email")
        password = request.POST.get("password")
        newpwd = request.POST.get("newpwd")
        connewpwd = request.POST.get("connewpwd")
        if tbllogin.objects.filter(email=uname, password=password).exists():
            lo = tbllogin.objects.get(email=uname, password=password)
            if newpwd == connewpwd:
                lo.password = newpwd
                lo.save()
                return HttpResponse("<script>alert('Successfully updated!!');window.location='/patient/changepassword'</script>")
            return HttpResponse("<script>alert('Password Mismatch !!');window.location='/patient/changepassword'</script>")
        return HttpResponse("<script>alert('Invalid Username orPassword!!');window.location='/patient/changepassword'</script>")
    return render(request, "patient/changepassword.html")

def editprofile(request):
    if request.method == 'POST':
        pat=patient.objects.get(loginid_id=request.session['loginid'])
        pat.patname = request.POST.get('patname')
        pat.email = request.POST.get('email')
        pat.phone = request.POST.get('phone')
        pat.gender = request.POST.get('gender')
        pat.age = request.POST.get('age')
        pat.housename = request.POST.get('housename')
        pat.pin = request.POST.get('pin')
        pat.opno = request.POST.get('opno')
        pat.locid = location.objects.get(locid=request.POST.get('locid'))

        pat.save()
        return HttpResponse("<script>alert('Successfully updated...');window.location='/patient/editprofile'</script>")
    pati=patient.objects.get(loginid_id=request.session['loginid'])
    dist=district.objects.all()
    loc= location.objects.filter(disid=pati.locid.disid.disid)
    return render(request, 'patient/editprofile.html',{ 'patient':pati, 'district': dist, 'location':loc})

def filllocation(request):
    id = int(request.POST.get("disid"))
    loc = location.objects.filter(disid=id).values()
    return JsonResponse(list(loc), safe=False)
def logout(request):
    if "loginid" in request.session:
        request.session.clear()
    return HttpResponse("<script>alert('successfully logout');window.location='/guest/home';</script>");
