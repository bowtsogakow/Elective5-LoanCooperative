
from django.urls import path
from admin_frontend import views

urlpatterns = [
    
  # admin front end 
  path("", views.index, name='index'), 
  
  
]