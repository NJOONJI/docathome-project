from django.urls import path
from . import views
from .views import ExportExcelHospital
from .views import ExportExcelDoctor
from .views import ExportExcelPatient


urlpatterns = [
    path('index/', views.index, name='index'),
    path('districtreg/', views.districtreg, name='districtreg'),
    path('locationreg/', views.locationreg, name='locationreg'),
    path('districtview/', views.districtview, name='districtview'),
    path('districtedit/<id>/', views.districtedit, name='districtedit'),
    path('deletedistrict/<id>/', views.deletedistrict, name="deletedistrict"),
    path('locationview/', views.locationview, name="locationview"),
    path("filllocation/", views.filllocation, name="filllocation"),
    path('locationedit/<id>/', views.locationedit, name='locationedit'),
    path('deletelocation/<id>/', views.deletelocation, name="deletelocation"),
    path('departmentreg/', views.departmentreg, name='departmentreg'),
    path('departmentview/', views.departmentview, name="departmentview"),
    path('departmentedit/<id>/', views.departmentedit, name='departmentedit'),
    path('deletedepartment/<id>/', views.deletedepartment, name="deletedepartment"),
    path('hospitalview/', views.hospitalview, name='hospitalview'),
    #path('fillhospital/', views.fillhospital, name='fillhospital'),
    path('fillhospital1/', views.fillhospital1, name='fillhospital1'),
    path('accepthospital/<id>/', views.accepthospital, name='accepthospital'),
    path('rejecthospital/<id>/', views.rejecthospital, name="rejecthospital"),
    path('patientview/', views.patientview, name='patientview'),
    path('fillpatient/', views.fillpatient, name='fillpatient'),
    path('acceptpatient/<id>/', views.acceptpatient, name='acceptpatient'),
    path('rejectpatient/<id>/', views.rejectpatient, name='rejectpatient'),
    path('doctorview/', views.doctorview, name='doctorview'),
    path('filldoctor/', views.filldoctor, name='filldoctor'),
    path('acceptdoctor/<id>/', views.acceptdoctor, name='acceptdoctor'),
    path('rejectdoctor/<id>/', views.rejectdoctor, name='rejectdoctor'),
    path('servicereg/', views.servicereg, name='servicereg'),
    path('serviceview/', views.serviceview, name='serviceview'),
    path('serviceedit/<id>/', views.serviceedit, name='serviceedit'),
    path('servicedelete/<id>/', views.servicedelete, name="servicedelete"),
    path('hosserviceview/', views.hosserviceview, name='hosserviceview'),
    path('hosservicedelete/<id>/', views.hosservicedelete, name="hosservicedelete"),
    path('hospitaldeptview/', views.hospitaldeptview, name='hospitaldeptview'),
    path('filldepartment/', views.filldepartment, name='filldepartment'),
    path('disreport/', views.disreport, name='disreport'),
    path("hospitalfill/", views.hospitalfill, name="hospitalfill"),
    path('hospitalcount_pie/', views.hospitalcount_pie, name='hospitalcount_pie'),
    path('patientbookreport/', views.patientbookreport, name='patientbookreport'),
    path('fillhospitaladmin/', views.fillhospitaladmin, name='fillhospitaladmin'),
    path('patientcount_pie/', views.patientcount_pie, name='patientcount_pie'),
    path('fillserviceadmin/', views.fillserviceadmin, name='fillserviceadmin'),
    path('hosdetailsreport/', views.hosdetailsreport, name='hosdetailsreport'),
    path('fillhosadmin/', views.fillhosadmin, name='fillhosadmin'),
    path('hospitaldetails/', ExportExcelHospital.as_view(), name='hospitaldetails'),
    path('doctordetreport/', views.doctordetreport, name='doctordetreport'),
    path('doctordetails/', ExportExcelDoctor.as_view(), name='doctordetails'),
    path('bookpatientreport/', views.bookpatientreport, name='bookpatientreport'),
    path('patientdetails/', ExportExcelPatient.as_view(), name='patientdetails'),
    path('logout/', views.logout, name='logout'),

    # sample url

    path('test/', views.test, name="test"),

]
