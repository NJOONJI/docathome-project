import smtplib
from email.message import EmailMessage

import xlwt
from django.db.models import Count
from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_control

from adminapp.models import *
from guest.models import hospital, tbllogin
# from guest.models import patient, tbllogin
from django.http import HttpResponse, JsonResponse

from hospitalapp.models import doctor, patient, hosservice
from patientapp.models import appointment


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if "loginid" in request.session:
        return render(request, "admin/index.html")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            disname = request.POST.get('disname')
            disobj = district()
            if district.objects.filter(disname=disname).exists():
                return HttpResponse("<script>alert('Duplicate..');window.location='/admin/districtreg';</script>")
            disobj.disname = disname
            disobj.save()
            return HttpResponse("<script>alert('Inserted..');window.location='/admin/districtreg';</script>")
        else:
            return render(request, "admin/districtreg.html")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            disname = request.POST.get('disname')
            # return HttpResponse(dep_name)
            locname = request.POST.get('locname')
            locobj = location()
            if location.objects.filter(disid=disname, locname=locname).exists():
                return HttpResponse("<script>alert('Duplicate..');window.location='/admin/locationreg';</script>")
            locobj.disid = district.objects.get(disid=disname)
            locobj.locname = locname
            locobj.save()
            return HttpResponse("<script>alert('Inserted..');window.location='/admin/locationreg';</script>")
        else:
            disname = district.objects.all()
            # return HttpResponse(dep_name)
            return render(request, 'admin/locationreg.html', {'district': disname})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/districtview.html", {"district": dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            disname = request.POST.get('disname')
            dist = district.objects.get(disid=id)
            dist.disname = disname
            dist.save()
            return districtview(request)
        dist = district.objects.get(disid=id)
        return render(request, "admin/districtedit.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedistrict(request, id):
    if "loginid" in request.session:
         dep = district.objects.get(disid=id)
         dep.delete()
         return districtview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/locationview.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def filllocation(request):
    did = (request.POST.get("did"))
    loc = location.objects.filter(disid=did).values()
    return JsonResponse(list(loc), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            locname = request.POST.get('locname')
            disname = request.POST.get('districtid')
            loc = location.objects.get(locid=id)
            loc.disid = district.objects.get(disid=disname)
            loc.locname = locname
            loc.save()

            return HttpResponse("<script>alert('Inserted..');window.location='/admin/locationview';</script>")
            return locationview(request)
        else:
            loc = location.objects.get(locid=id)
            dist = district.objects.all()
            return render(request, "admin/locationedit.html", {'loc': loc, 'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletelocation(request, id):
    if "loginid" in request.session:
        loc = location.objects.get(locid=id)
        loc.delete()
        return locationview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def departmentreg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            depname = request.POST.get('depname')
            depobj = department()
            if department.objects.filter(depname=depname).exists():
                return HttpResponse("<script>alert('Duplicate..');window.location='/admin/departmentreg';</script>")
            depobj.depname = depname
            depobj.depphoto = request.FILES['depphoto']
            depobj.save()
            return HttpResponse("<script>alert('Inserted..');window.location='/admin/departmentreg';</script>")
        else:
            return render(request, "admin/departmentreg.html")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def departmentview(request):
    if "loginid" in request.session:
        dept = department.objects.all()
        return render(request, "admin/departmentview.html", {'dept': dept})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def departmentedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            depname = request.POST.get('depname')
            dept = department.objects.get(depid=id)
            dept.depname = depname
            dept.save()
            return departmentview(request)
            dept = department.objects.get(depid=id)
            return render(request, "admin/departmentedit.html", {'dept': dept})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedepartment(request, id):
    if "loginid" in request.session:
        dept = department.objects.get(depid=id)
        dept.delete()
        return departmentview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def test(request):
    return render(request, "admin/test.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospitalview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/hospitalview.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


#
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillhospital1(request):
    if "loginid" in request.session:
        did = request.POST.get("did")
        # print("Received locid:", did)  # Add this line for debugging purposes

        hosid = hospital.objects.select_related('loginid').filter(locid=did, loginid__status="requested").values('hosname',
                                                                                                                 'regdate',
                                                                                                             'licencephoto',
                                                                                                             'hosid',
                                                                                                             'phone')
        # print("Query Result:", hosid)  # Add this line for debugging purposes


        return JsonResponse(list(hosid), safe=False)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accepthospital(request, id):
    if "loginid" in request.session:
        dist = hospital.objects.get(hosid=id)

        login = dist.loginid.loginid

        lob = tbllogin.objects.get(loginid=login)
        lob.status = 'accepted'
        lob.save()
        return HttpResponse("<script>alert('Accepted');window.location='/admin/hospitalview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejecthospital(request, id):
    if "loginid" in request.session:
        dist = hospital.objects.get(hosid=id)

        login = dist.loginid.loginid

        lob = tbllogin.objects.get(loginid=login)
        lob.status = 'rejected'
        lob.save()
        return HttpResponse("<script>alert('Rejected');window.location='/admin/hospitalview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patientview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/patientview.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


#
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillpatient(request):
    if "loginid" in request.session:
        did = request.POST.get("did")
        # print("Received locid:", did)  # Add this line for debugging purposes

        patid = patient.objects.filter(locid=did).values()
        # print("Query Result:", hosid)  # Add this line for debugging purposes

        return JsonResponse(list(patid), safe=False)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def acceptpatient(request, id):
    if "loginid" in request.session:
        pat = patient.objects.get(patid=id)
        loginid = pat.loginid.loginid
        # return HttpResponse(loginid)

        pat = tbllogin.objects.get(loginid=loginid)
        pat.status = 'Confirmed'
        pat.save()

        return HttpResponse("<script>alert('Confirmed');window.location='/admin/patientview';</script>")

        # return doctorview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectpatient(request, id):
    if "loginid" in request.session:
        pat = patient.objects.get(patid=id)
        loginid = pat.loginid.loginid
        # return HttpResponse(loginid)

        pat = tbllogin.objects.get(loginid=loginid)
        pat.status = 'Rejected'
        pat.save()
        return HttpResponse("<script>alert('Rejected');window.location='/admin/patientview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctorview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/doctorview.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


#
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filldoctor(request):
    if "loginid" in request.session:
        did = request.POST.get("did")
        # print("Received locid:", did)  # Add this line for debugging purposes
        docid = doctor.objects.filter(locid=did, loginid__status='requested').values()
        # print("Query Result:", hosid)  # Add this line for debugging purposes
        return JsonResponse(list(docid), safe=False)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def acceptdoctor(request, id):
    if "loginid" in request.session:
        doc = doctor.objects.get(docid=id)
        loginid = doc.loginid.loginid
        # return HttpResponse(loginid)

        doc = tbllogin.objects.get(loginid=loginid)
        doc.status = 'Confirmed'
        doc.save()

        return HttpResponse(
            "<script>alert('Confirmation Mail sent Successfully');window.location='/admin/doctorview';</script>")

        # return doctorview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectdoctor(request, id):
    if "loginid" in request.session:
        doc = doctor.objects.get(docid=id)
        loginid = doc.loginid.loginid
        # return HttpResponse(loginid)

        doc = tbllogin.objects.get(loginid=loginid)
        doc.status = 'Rejected'
        doc.save()
        return HttpResponse("<script>alert('Rejected');window.location='/admin/doctorview';</script>")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def servicereg(request):
    if "loginid" in request.session:
        if request.method == 'POST':
            serobj = service()
            sernamee = request.POST.get('sername')
            serobj.sername = sernamee
            serobj.serTime = request.POST.get('sertime')
            serobj.serphoto = request.FILES['serphoto']
            if service.objects.filter(sername=sernamee).exists():
                return HttpResponse("<script>alert('Already Exists ');window.location='/admin/servicereg';</script>")
            else:
                serobj.save()
                # hos = hospital.objects.all()
                return HttpResponse(
                    "<script>alert('Successfully Registerd ');window.location='/admin/servicereg';</script>")

        return render(request, "admin/servicereg.html")
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def serviceview(request):
    if "loginid" in request.session:
        ser = service.objects.all()
        return render(request, "admin/serviceview.html", {'ser': ser})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def serviceedit(request, id):
    if "loginid" in request.session:
        if request.method == 'POST':
            sername = request.POST.get('sername')
            serTime = request.POST.get('serTime')
            ser = service.objects.get(serid=id)
            ser.sername = sername
            ser.serTime = serTime
            ser.save()
            return serviceview(request)
        ser = service.objects.get(serid=id)
        return render(request, "admin/serviceedit.html", {'ser': ser})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def servicedelete(request, id):
    if "loginid" in request.session:
        ser = service.objects.get(serid=id)
        ser.delete()
        return serviceview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hosserviceview(request):
    if "loginid" in request.session:
        ser = service.objects.all()
        return render(request, "admin/hosserviceview.html", {'ser': ser})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hosservicedelete(request, id):
    if "loginid" in request.session:
        ser = service.objects.get(serid=id)
        ser.delete()
        return hosserviceview(request)
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospitaldeptview(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/hospitaldeptview.html", {'dist': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


#
def filldepartment(request):
    did = request.POST.get("did")
    # print("Received locid:", did)  # Add this line for debugging purposes

    depid = hospital.objects.select_related('loginid').filter(locid=did, loginid__status="requested").values('depname',
                                                                                                             'locname')
    # print("Query Result:", hosid)  # Add this line for debugging purposes

    return JsonResponse(list(depid), safe=False)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def disreport(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/disreport.html", {'district': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def hospitalfill(request):
    location = request.POST.get("loc")
    hosid = hospital.objects.filter(locid=location).values()
    return JsonResponse(list(hosid), safe=False)


def hospitalcount_pie(request):
    labels = []
    data = []
    districtid = request.POST.get('district')
    queryset = location.objects.filter(disid=districtid)
    s=[]
    for q in queryset:
        #return HttpResponse(q.locid)
        s=hospital.objects.filter(locid=q.locid).values('locid__locname').annotate(
        total_hospital=Count('hosid'))
    #return HttpResponse(s)
        for s1 in s:
            labels.append(s1['locid__locname'])
            data.append(s1['total_hospital'])
    #return HttpResponse(labels)
    return render(request, 'admin/disreportview.html', {
        'labels': labels,
        'data': data
    })
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patientbookreport(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/patientbookreport.html", {'district': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def fillhospitaladmin(request):
    loc =int(request.POST.get("loc"))
    hosid = hospital.objects.filter(locid_id=loc).values()
    return JsonResponse(list(hosid), safe=False)


def patientcount_pie(request):
    labels = []
    data = []
    hosname = request.POST.get('hosname')
    #return HttpResponse(hosname)
    queryset = appointment.objects.filter(docid__hosid_id=hosname,status="Assigned").values('hosserid__serid__sername').annotate(total_appointment=Count('appid'))
    #return HttpResponse(queryset)
    for q in queryset:
        #return HttpResponse(q.locid)
        labels.append(q['hosserid__serid__sername'])
        data.append(q['total_appointment'])
    #return HttpResponse(labels)
    return render(request, 'admin/servicecount.html', {
        'labels': labels,
        'data': data
    })

def fillserviceadmin(request):
    hos =int(request.POST.get("loc"))
    serid = hosservice.objects.filter(hospitalid_id=hos).values('serid__sername','serid__serid')
    return JsonResponse(list(serid), safe=False)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hosdetailsreport(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/hosdetailsreport.html", {'district': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


def fillhosadmin(request):
    loc =int(request.POST.get("loc"))
    hosid = hospital.objects.filter(locid_id=loc).values()
    return JsonResponse(list(hosid), safe=False)


class ExportExcelHospital(View):
    def post(self, request):
        location=request.POST.get('location')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="hospitaldetails.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Id','Name', 'Phone No', 'Mail id','Status']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = hospital.objects.filter(locid_id=location).values_list('hosid','hosname', 'phone', 'loginid__email','loginid__status')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctordetreport(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/doctordetreport.html", {'district': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


class ExportExcelDoctor(View):
    def post(self, request):
        hosname=request.POST.get('hosname')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="doctordetails.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Id','Name', 'Phone No', 'Qualification','Experience','Specialization','Online Time','Mail id','Department']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = doctor.objects.filter(hosid_id=hosname).values_list('docid','docname', 'phone','qualification','experience','specialization','OnlineTime','loginid__email','depid__depname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bookpatientreport(request):
    if "loginid" in request.session:
        dist = district.objects.all()
        return render(request, "admin/bookpatientreport.html", {'district': dist})
    return HttpResponse("<script>alert('Authentication Required..');window.location='/guest/login/';</script>")


class ExportExcelPatient(View):
    def post(self, request):
        sername=request.POST.get('sername')
        fdate=request.POST.get('fdate')
        tdate=request.POST.get('tdate')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patientdetails.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Id','Name', 'Phone No', 'Email','Gender','Age','House Name','Pin','Op No']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = appointment.objects.filter(appdate__range=(fdate,tdate),status="Completed",hosserid__serid_id=sername).values('patid_id').distinct()
        for q in queryset:
            #return HttpResponse(q['patid_id'])
            pdetails=patient.objects.filter(patid=q['patid_id']).values_list('patid','patname','phone','email','gender','age','housename','pin','opno')
            for row in pdetails:
                row_num += 1
                for col_num, cell_value in enumerate(row):
                    ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response
def logout(request):
    if "loginid" in request.session:
        request.session.clear()
    return HttpResponse("<script>alert('successfully logout');window.location='/guest/home';</script>");

