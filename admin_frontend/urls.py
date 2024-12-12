
from django.urls import path
from admin_frontend import views

urlpatterns = [
    
  # admin front end 

  # client
  path("", views.index, name="admin_index"), 
  path("clients", views.client_list_page, name="client_list"),
  path("clients/<int:id>", views.client_info_page, name="client_info"),
  path("clients/add", views.add_client_page, name="client_add"),

  # loan
  path("loans", views.loan_list_page, name="loan_list"),
  path("loans/add", views.add_loan_page, name="loan_add"),
  path("loans/<int:id>", views.loan_info_page, name="loan_info"),

  # employee
  path("employees", views.employee_list_page, name="employee_list"),
  path("employees/add", views.add_employee_page, name = "employee_add"),

  # profile page 
  path("profile", views.profile_page, name = "profile_info"),
  
  
  
]