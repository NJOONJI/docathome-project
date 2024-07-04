from django.urls import path
from .import views

urlpatterns = [

    path('home/', views.index,name='home'),
    path('servicebooking/', views.servicebooking, name='servicebooking'),
    path('fillservices/', views.fillservices, name='fillservices'),
    path('hosservice/<id>', views.hosserviceview, name='hosservice'),
    path('servicerequest/<id>', views.servicerequest, name='servicerequest'),
    path('bookingconfirmation/', views.bookingconfirmation, name='bookingconfirmation'),
    path('viewmoreconfirmation/<id>', views.viewmoreconfirmation, name='viewmoreconfirmation'),
    path('viewmorerejection/<id>', views.viewmorerejection, name='viewmorerejection'),
    path('viewcasehistory/', views.viewcasehistory, name='viewcasehistory'),
    path('fillhospital/', views.fillhospital, name='fillhospital'),
    path('complaintreg/', views.complaintreg,name='complaintreg'),
    path('complaintnew/<id>', views.complaintnew,name='complaintnew'),
    path('deletecomplaint/<id>', views.deletecomplaint,name='deletecomplaint'),
    path('feedbackreg/', views.feedbackreg,name='feedbackreg'),
    path('feedbacknew/<id>', views.feedbacknew,name='feedbacknew'),
    path('deletefeedback/<id>', views.deletefeedback,name='deletefeedback'),
    path('changepassword', views.changepassword,name='changepassword'),
    path('editprofile',views.editprofile,name="editprofile"),
    path('logout/', views.logout, name='logout'),






]