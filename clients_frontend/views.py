from django.shortcuts import render
from admin_frontend.configurations import base_url
import requests
from django.urls import reverse
from server.decorators import client_required

# Create your views here.

@client_required
def index(request): 
    id = request.user.id
    path_loan_info = reverse('server_get_latest_loan_by_client', args=[id])
    url = f"{base_url}{path_loan_info}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == 2: 
        has_loan = False
        loan = None
 
    elif data["status"] == 1:
        has_loan = True
        loan = data["loan"]

    path_get_loan_by_client = reverse('server_get_loan_list_by_client', args=[id])
    url_get_loan_by_client = f"{base_url}{path_get_loan_by_client}"
    response_get_loan_by_client = requests.get(url_get_loan_by_client)
    data_get_loan_by_client = response_get_loan_by_client.json()

    path_get_payment_by_client = reverse('server_get_payment_list_by_client', args=[id])
    url_get_payment_by_client = f"{base_url}{path_get_payment_by_client}"
    response_get_payment_by_client = requests.get(url_get_payment_by_client)
    data_get_payment_by_client = response_get_payment_by_client.json()

    return render(request, 'clients_frontend/index.html', {
        "has_loan" : has_loan, 
        "loan" : loan,
        "loan_list" : data_get_loan_by_client["loans"],
        "payments" : data_get_payment_by_client["payments"]
    })


@client_required
def profile_page(request):
    id = request.user.id
    path = reverse('server_get_employee_by_id', args=[id])
    url = f"{base_url}{path}"
    response = requests.get(url)
    data = response.json()
    return render(request, 'clients_frontend/profileInfo.html', {"client" : data["employee"]})
 