import datetime
import smtplib
from email.message import EmailMessage

from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import cache_control

from guest.models import patient
from hospitalapp.models import *
from adminapp.models import *

from django.http import HttpResponse, JsonResponse

from patientapp.models import appointment, patienthistory, feedback
from datetime import datetime
from django.utils import timezone
from datetime import timedelta


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        dis = district.objects.all()
        return render(request, "hospital/index.html", {'dis': dis})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctorreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            lob = tbllogin()
            lob.email = request.POST.get('email')
            lob.password = request.POST.get('password')
            lob.role = 'doctor'
            lob.status = 'cofirmed'
            if tbllogin.objects.filter(email=request.POST.get('email')).exists():
                return HttpResponse("<script>alert('Email Already Exixts');window.location='/hospital/doctorreg';</script>")
            else:
                lob.save()
                docnamee = request.POST.get('docname')
                phone = request.POST.get('phone')
                docobj = doctor()
                docobj.docname = docnamee
                docobj.qualification = request.POST.get('qualificationn')
                docobj.experience = request.POST.get('experience')
                docobj.specialization = request.POST.get('specialization')
                docobj.OnlineTime = request.POST.get('OnlineTime')
                docobj.email = request.POST.get('email')
                docobj.phone = phone
                docobj.locid = location.objects.get(locid=request.POST.get('locname'))
                docobj.depid = department.objects.get(depid=request.POST.get('depname'))
                docobj.hosid = hospital.objects.get(loginid=request.session['loginid'])
                docobj.loginid = lob
                docobj.save()
                content = "Your mail id is " + lob.email + " and  Password is " + lob.password
                msg = EmailMessage()
                msg.set_content(content)
                msg['Subject'] = "Doctor confirmation details"
                msg['from'] = 'albybennichen15@gmail.com'
                msg['To'] = lob.email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('albybennichen15@gmail.com', 'hqmo pbhe uyhl yvxm')
                    smtp.send_message(msg)
                return HttpResponse(
                    "<script>alert('Successfully Registerd and confirmation Mail Send');window.location='/hospital/doctorreg';</script>")

        else:
            dis = district.objects.all()
            dept = department.objects.all()
            # return HttpResponse(dept)

            return render(request, "hospital/doctorreg.html", {'dis': dis, 'department': dept})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def filllocation(request):
    did = (request.POST.get("did"))
    loc = location.objects.filter(disid=did).values()
    return JsonResponse(list(loc), safe=False)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hosservicereg(request):
    if "loginid" in request.session:
        ser = service.objects.all()
        hosser = hosservice.objects.filter(hospitalid__loginid_id=request.session['loginid']).values_list('serid_id', flat=True)
        services_with_flag = [{'service': s, 'associated': s.serid in hosser} for s in ser]
        return render(request, "hospital/hosservicereg.html", {'services_with_flag': services_with_flag})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addhosservice(request,id):
    if "loginid" in request.session:
        hob=hosservice()
        hob.serid=service.objects.get(serid=id)
        hob.hospitalid=hospital.objects.get(loginid_id=request.session['loginid'])
        hob.save()
        return HttpResponse("<script>alert('Services Assigned Successfully');window.location='/hospital/hosservicereg';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patientservicerequest(request):
    if "loginid" in request.session:
        services=hosservice.objects.filter(hospitalid__loginid_id=request.session['loginid'])
        #return HttpResponse(apprequests)
        return render(request, "hospital/patientservicerequest.html", {'services': services})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def viewmoredetails(request,id):
    details=appointment.objects.filter(hosserid_id=id,status="Requested")
    return render(request, "hospital/viewmoredetails.html",{'details':details})
def viewmorerequest(request,id):
    details=appointment.objects.get(appid=id)
    dept=hospitaldepartment.objects.filter(hosid__loginid_id=request.session['loginid'])
    #return HttpResponse(details.patid.patid)
    today_date = date.today()
    return render(request, "hospital/viewmorerequest.html",{'today_date':today_date,'dept':dept,'details':details})
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospitaldeptreg(request):
    if "loginid" in request.session:
            if request.method == "POST":
                hob=hospitaldepartment()
                hob.depid=department.objects.get(depid=request.POST.get('depname'))
                hob.hosid=hospital.objects.get(loginid_id=request.session['loginid'])
                if hospitaldepartment.objects.filter(depid=department.objects.get(depid=request.POST.get('depname')),hosid=hospital.objects.get(loginid_id=request.session['loginid'])).exists():
                    return HttpResponse(
                        "<script>alert('Already Exists');window.location='/hospital/hospitaldeptreg';</script>")
                else:
                    hob.save()
                    return HttpResponse("<script>alert('Successfully Registerd');window.location='/hospital/hospitaldeptreg';</script>")
            dept=department.objects.all()
            return render(request, "hospital/hospitaldeptreg.html",{'dept':dept})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def filldoctor(request):
    did=(request.POST.get("did"))
   #adate=request.POST.get("adate")
    loc=doctor.objects.filter(depid_id =did).values()
    #adate_obj = datetime.strptime(adate, "%B %d, %Y").date()
    #return HttpResponse(loc)
    # doc=list()
    # for l in loc :
    #     if not appointment.objects.filter(docid=l['docid'], appdate=adate_obj).exists():
    #         #return HttpResponse(adate_obj)
    #         doc.append({'docid': l['docid'], 'docname': l['docname']})
    # #return HttpResponse("hello")
    #return HttpResponse(doc)
    return JsonResponse(list(loc),safe=False)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def assigndoctor(request,id):
    if "loginid" in request.session:
        aob=appointment.objects.get(appid=id)
        aob.docid=doctor.objects.get(docid=request.POST.get('docname'))
        aob.status="Assigned"
        aob.save()
        return HttpResponse("<script>alert('Successfully Assigned Doctor');window.location='/hospital/patientservicerequest';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def appointmentdetails(request):
    if "loginid" in request.session:
        did = (request.POST.get("did"))
        adate = request.POST.get("adate")
        adate_obj = datetime.strptime(adate, "%B %d, %Y").date()
        loc = appointment.objects.filter(docid=did,appdate=adate_obj,status="Assigned").values()
        return JsonResponse(list(loc), safe=False)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectrequest(request,id):
    if "loginid" in request.session:
        aob=appointment.objects.get(appid=id)
        aob.status="Rejected"
        aob.remark=request.POST.get('reason')
        aob.save()
        return HttpResponse(
            "<script>alert('Successfully Rejected');window.location='/hospital/patientservicerequest';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addcasehistory(request):
    if "loginid" in request.session:
        yesterday = timezone.now().date() - timedelta(days=1)

        details=appointment.objects.filter(status="Assigned",appdate__lte=yesterday)
        #return HttpResponse(details)
        return render(request, "hospital/addcasehistory.html",{'details':details})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def fillpatient(request):
    did = (request.POST.get("did"))
    loc = patient.objects.filter(opno=did).values('patid','patname','email','gender','age','phone','pin','housename','regdate','opno','locid__locname',)
    return JsonResponse(list(loc), safe=False)
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def insertcasehistory(request,id):
    if "loginid" in request.session:
        if request.method == "POST":

            pob = patienthistory()
            pob.description = request.POST.get('description')
            pob.symptoms = request.POST.get('symptoms')
            pob.prescription = request.POST.get('prescription')

            pob.appid = appointment.objects.get(appid=id)

            if patienthistory.objects.filter(appid = appointment.objects.get(appid=id)).exists():
                return HttpResponse("<script>alert('Already Exists');window.location='/hospital/addcasehistory';</script>")
            else:
                pob.save()
                obj=appointment.objects.get(appid=id)
                obj.status="Completed"
                obj.save()
                return HttpResponse(
                    "<script>alert('Case history Successfully Inserted');window.location='/hospital/addcasehistory';</script>")

        return render(request, "hospital/insertcasehistory.html",{'appid':id})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def complaintview(request):
    if "loginid" in request.session:
        comp = complaint.objects.all()
        return render(request, "hospital/complaintview.html", {"complaint": comp})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecomplaint(request, id):
    if "loginid" in request.session:
        comp = complaint.objects.get(compid=id)
        comp.delete()
        return HttpResponse(
            "<script>alert('Complaint Successfully Deleted');window.location='/hospital/complaintview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedbackview(request):
    if "loginid" in request.session:
        feed = feedback.objects.all()
        return render(request, "hospital/feedbackview.html", {"feedback": feed})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword(request):
    if "loginid" in request.session:
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
                    return HttpResponse("<script>alert('Successfully updated!!');window.location='/hospital/changepassword'</script>")
                return HttpResponse("<script>alert('Password Mismatch !!');window.location='/hospital/changepassword'</script>")
            return HttpResponse("<script>alert('Invalid Username orPassword!!');window.location='/hospital/changepassword'</script>")
        return render(request, "hospital/changepassword.html")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editprofile(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            hos=hospital.objects.get(loginid_id=request.session['loginid'])
            hos.hospitalname = request.POST.get('hosname')
            hos.email = request.POST.get('email')
            hos.address = request.POST.get('address')
            hos.phone = request.POST.get('phone')
            hos.locid = location.objects.get(locid=request.POST.get('locid'))
            if 'himagenew' in request.FILES:
                hos.hosphoto =  request.FILES['himagenew']
            else:
                hos.hosphoto =request.POST.get('himage')
            if 'hosliscencenew' in request.FILES:
                hos.licencephoto = request.FILES['hosliscencenew']
            else:
                hos.licencephoto = request.POST.get('hosliscence')

            hos.save()
            return HttpResponse("<script>alert('Successfully updated...');window.location='/hospital/editprofile'</script>")
        hosp=hospital.objects.get(loginid_id=request.session['loginid'])
        dist=district.objects.all()
        loc= location.objects.filter(disid=hosp.locid.disid.disid)
        return render(request, 'hospital/editprofile.html',{ 'hospital':hosp, 'district': dist, 'location':loc})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def filllocation(request):
    id = int(request.POST.get("disid"))
    loc = location.objects.filter(disid=id).values()
    return JsonResponse(list(loc), safe=False)
def logout(request):
    if "loginid" in request.session:
        request.session.clear()
    return HttpResponse("<script>alert('successfully logout');window.location='/guest/home';</script>");


