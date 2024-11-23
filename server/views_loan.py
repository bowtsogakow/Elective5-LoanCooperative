from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from server.models import Loan, User

@api_view(["POST"])
def add_loan(request): 
    client_id = request.data.get("client_id")
    loan_term = request.data.get("loan_term")
    amount_loaned = request.data.get("amount_loaned")
    interest_percentage = request.data.get("interest_percentage")
    interest_mode = request.data.get("interest_mode")
    type = "loan"

    if not client_id or not loan_term or not amount_loaned or not interest_percentage or not interest_mode:
        return Response({
            "status" : 0,
            "status_message" : "Missing invalid input"
        })

    client = User.objects.filter(id = client_id, type = "client").first()

    if not client : 
        return Response({
            "status" : 0,
            "status_message" : "Client does not exist"
        })

    loan = Loan.objects.filter(client = client, status = "ongoing").first()

    if loan : 
        return Response({
            "status" : 0,
            "status_message" : "Client has an existing loan"
        })

    try : 
        new_loan = Loan(client = client, 
                        loan_term = loan_term, 
                        amount_loaned = amount_loaned, 
                        interest_percentage = interest_percentage, 
                        interest_mode = interest_mode)    
        
        new_loan.compute_and_save()

    except Exception as e : 
        return Response({
            "status" : 0,
            "status_message" : str(e)
        })

    return Response({
        "status" : 1,
        "status_message" : "Loan added successfully"
    })

@api_view(["GET"])
def get_ongoing_loans(request):
    loans = Loan.objects.filter(status = "ongoing").order_by