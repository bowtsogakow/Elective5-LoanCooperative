import uuid
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageUploadForm, LoanForm
from django.utils.timezone import now
from .models import Client, Loan
import qrcode 
from .utils import generate_qr_code

#This is for setting up the front end alone

def index(request):
  return render(request, 'AgriTrust/index.html')

def registerClient(request):
  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():

      billing_statement_electric = request.FILES.get('billing_statement_electric')
      billing_statement_water = request.FILES.get('billing_statement_water')
      name = request.POST.get('name')
      
      # Rename the files before saving
      if billing_statement_electric:
          extension = billing_statement_electric.name.split('.')[-1]
          new_filename = f"{uuid.uuid4().hex}_{now().strftime('%Y%m%d%H%M%S')}.{extension}"
          billing_statement_electric.name = new_filename  # Rename the file
      
      if billing_statement_water:
          extension = billing_statement_water.name.split('.')[-1]
          new_filename = f"{uuid.uuid4().hex}_{now().strftime('%Y%m%d%H%M%S')}.{extension}"
          billing_statement_water.name = new_filename  # Rename the file

     
      client = form.save(commit=False)
      
      if billing_statement_electric:
          client.billing_statement_electric = billing_statement_electric
      if billing_statement_water:
          client.billing_statement_water = billing_statement_water
      
      
      client.save()

      return HttpResponse('success')

  else:
    form = ImageUploadForm()

  return render(request, 'AgriTrust/registerCLient.html', {'form': form})

def registerLoan(request):
  if request.method == 'POST':
      form = LoanForm(request.POST)
      client_id = request.POST.get('client')
      if form.is_valid():
        loan = form.save(commit=False)
        client = Client.objects.filter(id=client_id).first()

        if client:
          if client.co_maker == None:
            return HttpResponse('Please add co-maker of the client')
          
          loan_db = Loan.objects.filter(client__id = client_id, status = "ongoing").first()

          if loan_db : 
            return HttpResponse('Client has ongoing loan')
          
          loan.save()

          loan_db = Loan.objects.filter(client__id = client_id, status = "ongoing").first()
          qr_code_image = generate_qr_code(loan_db.qr_code)
          print(qr_code_image)

          return render(request, 'AgriTrust/registerLoan.html', {'qr_code_image' : qr_code_image})
        
        return HttpResponse('Client not found')

  else: 
    form =  LoanForm()
  return render(request, 'AgriTrust/registerLoan.html', {'form': form})


# def payLOan