from django.shortcuts import render
from django.urls import reverse
import requests
from server.decorators import cashier_required
from admin_frontend.configurations import base_url
# Create your views here.

@cashier_required
def index(request): 
    return render(request, 'cashier_frontend/index.html')

@cashier_required
def profile_page(request, id): 
  path = reverse('server_get_employee_by_id', args=[id])
  url = f"{base_url}{path}"
  response = requests.get(url)
  data = response.json()
  return render(request, 'cashier_frontend/profileInfo.html', {"employee" : data["employee"]})