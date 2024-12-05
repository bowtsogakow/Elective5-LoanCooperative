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


# dashboard 
# 
def index(request):
  return render(request, 'AgriTrust/index.html')

# clients 
def client_list_page(request): 
  path = reverse('server_get_all_clients')
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'AgriTrust/clients.html', {"clients" : data["clients"]})

def client_info_page(request, id): 
  path = reverse('server_get_client_by_id', args=[id])
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  
  return render(request, 'AgriTrust/clientInfo.html', {"client" : data["client"]})
  
def add_client_page(request): 

  return render(request, 'AgriTrust/registerClient.html')

def loan_list_page(request): 
  path = reverse('server_get_all_loans')
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'AgriTrust/loans.html', {"loans" : data["loans"]})

def loan_info_page(request, id): 
  path = reverse('server_get_loan_by_id', args=[id])
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'AgriTrust/loanInfo.html', {"loan" : data["loan"]})

def add_loan_page(request):
  
  loan_terms_choices = Loan.LOAN_TERMS
  interest_mode_choices = Loan.INTEREST_MODE_CHOICES
  return render(request, 'AgriTrust/registerLoan.html', 
    {"loan_terms_choices" : loan_terms_choices, 
     "interest_mode_choices" : interest_mode_choices})

def user_page(request): 
  return None


