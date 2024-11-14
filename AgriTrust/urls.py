
from django.urls import path
from django.contrib import admin
from AgriTrust import views

urlpatterns = [
  path("", views.index, name='index'),
  path("client/register", views.registerClient, name='register'),
  path("loan/create", views.registerLoan, name='registerLoan'),
  
]