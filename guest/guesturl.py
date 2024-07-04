from django.urls import path
from .import views

urlpatterns = [

path('login/', views.login,name='login'),
path('home/', views.index,name='home'),
path('hospitalreg/', views.hospitalreg,name='hospitalreg'),
path('patientreg/', views.patientreg,name='patientreg'),
path('forgotpassword/', views.forgotpassword,name='forgotpassword'),


]