from django.urls import path
from .import views

urlpatterns = [

path('home/', views.index,name='home'),
path('doctorreg/', views.doctorreg,name='doctorreg'),
path('hosservicereg/', views.hosservicereg,name='hosservicereg'),
path('addhosservice/<id>', views.addhosservice,name='addhosservice'),
path('patientservicerequest/', views.patientservicerequest, name='patientservicerequest'),
path('viewmoredetails/<id>', views.viewmoredetails, name='viewmoredetails'),
path('viewmorerequest/<id>', views.viewmorerequest, name='viewmorerequest'),
path('hospitaldeptreg/', views.hospitaldeptreg, name='hospitaldeptreg'),
path('filldoctor/', views.filldoctor, name='filldoctor'),
path('assigndoctor/<id>', views.assigndoctor, name='assigndoctor'),
path('appointmentdetails/', views.appointmentdetails, name='appointmentdetails'),
path('rejectrequest/<id>', views.rejectrequest, name='rejectrequest'),
path('addcasehistory/', views.addcasehistory, name='addcasehistory'),
path('fillpatient/', views.fillpatient, name='fillpatient'),
path('insertcasehistory/<id>', views.insertcasehistory, name='insertcasehistory'),
path('complaintview', views.complaintview, name='complaintview'),
path('deletecomplaint/<id>', views.deletecomplaint,name='deletecomplaint'),
path('feedbackview', views.feedbackview, name='feedbackview'),
path('changepassword', views.changepassword, name='changepassword'),
path('editprofile',views.editprofile,name="editprofile"),
path('logout/', views.logout, name='logout'),





]