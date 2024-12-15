import datetime
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
                        amount_loaned = float(amount_loaned), 
                        interest_percentage = float(interest_percentage), 
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
def get_all_loans(request):
    loans = Loan.objects.filter(status = "ongoing").order_by("-date_created")
    print(loans)
    
    response = []
    for loan in loans :
        
        days_passed = (datetime.date.today() - loan.date_created).days
        payment_position = days_passed - loan.days_paid

        data = {
            "id" : loan.id,
            "client_name" : loan.client.full_name,
            "amount" : loan.amount_loaned, 
            "status" : loan.status, 
            "start_date" : loan.date_created,
            "end_date" : loan.date_end,
            "daily_payment" : loan.daily_payment, 
            "days_left" : loan.days_total - loan.days_paid, 
            "payment_position" : payment_position
        }

        response.append(data)

    return Response({
        "status" : 1,   
        "status_message" : "Loans retrieved successfully",
        "loans" : response
    })


@api_view(["GET"])
def get_loan_by_id(request, loan_id):
    loan = Loan.objects.filter(id = loan_id).first()

    if not loan : 
        return Response({
            "status" : 0,
            "status_message" : "Loan does not exist"
        })
    
    data = {
        "id" : loan.id,
        "client_name" : loan.client.full_name,
        "amount_loaned" : loan.amount_loaned, 
        "interest_percentage" : loan.interest_percentage,
        "loan_term" : loan.loan_term,
        "interest_mode" : loan.interest_mode,
        "interest" : loan.interest,
        "total" : loan.total,
        "days_total" : loan.days_total,
        "days_paid" : loan.days_paid,
        "total_amount_paid" : loan.total_amount_paid,
        "status" : loan.status, 
        "date_created" : loan.date_created,
        "date_end" : loan.date_end,
        "daily_payment" : loan.daily_payment, 
        "days_left" : loan.days_total - loan.days_paid,
        "qr_code" : loan.qr_code
    }

    return Response({
        "status" : 1,   
        "status_message" : "Loan retrieved successfully",
        "loan" : data
    })


@api_view(["GET"])
def get_loan_list_by_client(request, client_id): 
    client = User.objects.filter(id = client_id).first()

    print(client)

    if not client : 
        return Response({
            "status" : 0,
            "status_message" : "Client not found"
        })
    
    loans = Loan.objects.filter(client = client)

    response = []

    for loan in loans : 
        data = {
            "id" : loan.id,
            "amount" : loan.amount_loaned, 
            "interest_percentage" : loan.interest_percentage,
            "loan_term" : loan.loan_term,
            "total" : loan.total,
            "status" : loan.status, 
            "date_created" : loan.date_created,
            "date_end" : loan.date_end,
        }

        response.append(data)

    return Response({
        "status" : 1,   
        "status_message" : "Loans retrieved successfully",
        "loans" : response
    })


@api_view(["POST"])
def get_loan_by_code(request):
    qr_code = request.data.get("qr_code")

    if not qr_code : 
        return Response({
            "status" : 0,
            "status_message" : "QR code is required"
        })
    
    loan = Loan.objects.filter(qr_code = qr_code).first()

    if not loan : 
        return Response({
            "status" : 0,
            "status_message" : "Loan does not exist"
        })

    data = {
        "id" : loan.id,
        "client_name" : loan.client.full_name,
        "daily_payment" : loan.daily_payment,
        "balance" : loan.total - loan.total_amount_paid,
    }

    return Response({
        "status" : 1,   
        "status_message" : "Loan retrieved successfully",
        "loan" : data
    })