import datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum
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


@api_view(["POST"])
def add_payment(request): 
    loan_id = request.data.get("loan_id")

    if not loan_id: 
        return Response({
            "status": 0, 
            "status_message": "Invalid input"
            })
    
    loan = Loan.objects.filter(id = loan_id).first()

    if not loan: 
        return Response({
            "status": 0, 
            "status_message": "Loan not found"
            })

    payment = Payment(amount = loan.daily_payment, loan = loan)
    payment.update_loan_and_save()

    loan = Loan.objects.filter(id = loan_id).first()

    return Response({ 
        "status" : 1, 
        "status_message": "Loan paid successfully",
        "remaining_balance" : loan.total - loan.total_amount_paid
    })


@api_view(["GET"])
def get_payment_table(request):

    result = []
    for i in range(6, -1, -1):
        days_ago = timezone.now() - datetime.timedelta(days=i)
        print(days_ago)
        payments = Payment.objects.filter(date=days_ago)
        amount = 0
        for payment in payments : 
            amount = payment.amount + amount
        result.append({
            "date" : days_ago.strftime('%Y-%m-%d'),
            "total_amount" : amount
        })

    return Response({
        "status" : 0, 
        "status_message" : "Success",
        "result" : result
    })