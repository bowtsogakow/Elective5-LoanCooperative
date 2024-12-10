import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from server.models import Loan, User, Payment 

@api_view(["GET"])
def get_payment_list_by_client(request, client_id):
    client = User.objects.filter(id = client_id).first()

    if not client:
        return Response({
            "status": 0, 
            "status_message": "Client not found"
            })
    
    loans = Loan.objects.filter(client = client) 

    response = []

    for loan in loans: 
        payments = Payment.objects.filter(loan = loan)

        for payment in payments :
            data = {
                "id": payment.id,
                "amount": payment.amount,
                "date": payment.date,
            }

            response.append(data)

    return Response({
        "status": 1,
        "status_message": "Payments retrieved successfully",
        "payments": response
    })


@api_view(["GET"])
def get_payment_list_by_loan(request, loan_id):
    loan = Loan.objects.filter(id = loan_id).first()

    if not loan:
        return Response({
            "status": 0, 
            "status_message": "Loan not found"
            })
    
    payments = Payment.objects.filter(loan = loan)

    response = []

    for payment in payments :
        data = {
            "id": payment.id,
            "amount": payment.amount,
            "date": payment.date,
        }

        response.append(data)

    return Response({
        "status": 1,
        "status_message": "Payments retrieved successfully",
        "payments": response
    })
