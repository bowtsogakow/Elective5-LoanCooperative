import uuid
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
import qrcode 
from .utils import generate_qr_code
from django.urls import reverse
import requests
from .configurations import base_url
from server.models import Loan
from server.decorators import admin_required

# dashboard 

@admin_required
def index(request):
  return render(request, 'AgriTrust/index.html')

# clients 
@admin_required
def client_list_page(request): 
  path = reverse('server_get_client_by_search')
  url = f"{base_url}{path}"
  response = requests.post(url, data={"pagination" : 1, "loan_status" : "both"})
  data = response.json()
  return render(request, 'AgriTrust/clients.html', {"clients" : data["clients"]})

@admin_required
def client_info_page(request, id): 
  path_client_info = reverse('server_get_client_by_id', args=[id])
  url_client_info = f"{base_url}{path_client_info}"
  response_client_info = requests.get(url_client_info)
  data_client_info = response_client_info.json()

  path_get_loan_by_client = reverse('server_get_loan_list_by_client', args=[id])
  url_get_loan_by_client = f"{base_url}{path_get_loan_by_client}"
  response_get_loan_by_client = requests.get(url_get_loan_by_client)
  data_get_loan_by_client = response_get_loan_by_client.json()

  path_get_payment_by_client = reverse('server_get_payment_list_by_client', args=[id])
  url_get_payment_by_client = f"{base_url}{path_get_payment_by_client}"
  response_get_payment_by_client = requests.get(url_get_payment_by_client)
  data_get_payment_by_client = response_get_payment_by_client.json()
  
  return render(request, 'AgriTrust/clientInfo.html', {
    "client" : data_client_info["client"],
    "loans" : data_get_loan_by_client["loans"],
    "payments" : data_get_payment_by_client["payments"]
  })

@admin_required
def add_client_page(request): 
  path = reverse('server_get_all_clients')
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'AgriTrust/registerClient.html', {
    "comakers" : data["clients"]
  })

@admin_required
def loan_list_page(request): 
  path = reverse('server_get_loans_by_search')
  url = f"{base_url}{path}"
  response = requests.post(url)
  data = response.json()
  return render(request, 'AgriTrust/loans.html', {"loans" : data["loans"]})

@admin_required
def loan_info_page(request, id): 
  path_loan_info = reverse('server_get_loan_by_id', args=[id])
  url_loan_info = f"{base_url}{path_loan_info}"
  response_loan_info = requests.get(url_loan_info)
  data_loan_info = response_loan_info.json()

  path_payment_info = reverse('server_get_payment_list_by_loan', args=[id])
  url_payment_info = f"{base_url}{path_payment_info}"
  response_payment_info = requests.get(url_payment_info)
  data_payment_info = response_payment_info.json()

  return render(request, 'AgriTrust/loanInfo.html', {
    "loan" : data_loan_info["loan"], 
    "payments" : data_payment_info["payments"]
    
    })

@admin_required
def add_loan_page(request):
  path = reverse('server_get_eligible_clients_for_loan')
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()

  loan_terms_choices = Loan.LOAN_TERMS
  interest_mode_choices = Loan.INTEREST_MODE_CHOICES
  return render(request, 'AgriTrust/registerLoan.html', 
    {"loan_terms_choices" : loan_terms_choices, 
     "interest_mode_choices" : interest_mode_choices, 
     "clients" : data["clients"]})

@admin_required
def employee_list_page(request):
  path = reverse('server_get_employee_by_search')
  url = f"{base_url}{path}"
  response = requests.post(url, data={"pagination" : 1, "type" : "all"})
  data = response.json()
  return render(request, 'AgriTrust/employees.html', {"employees" : data["employees"]})

@admin_required
def add_employee_page(request):
  return render(request, 'AgriTrust/registerEmployee.html')

@admin_required
def profile_page(request, id): 
  path = reverse('server_get_employee_by_id', args=[id])
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'AgriTrust/profileInfo.html', {"employee" : data["employee"]})


