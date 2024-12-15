from django.shortcuts import render
from server.decorators import cashier_required

# Create your views here.

@cashier_required
def index(request): 
    return render(request, 'cashier_frontend/index.html')