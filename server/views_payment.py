import datetime
import math
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum
from server.models import Loan, User, Payment 
from decimal import Decimal
from django.db.models import Q
from .utils import parse_date, format_number_with_commas

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
                "amount": format_number_with_commas(payment.amount),
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
            "amount": format_number_with_commas(payment.amount),
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
    amount = request.data.get("amount")

    if not loan_id: 
        return Response({
            "status": 0, 
            "status_message": "Invalid input"
            })
    
    if not amount and amount <= 0: 
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

    payment = Payment(amount = Decimal(amount), loan = loan)
    payment.update_loan_and_save()

    loan = Loan.objects.filter(id = loan_id).first()

    return Response({ 
        "status" : 1, 
        "status_message": "Loan paid successfully",
        "remaining_balance" : format_number_with_commas(loan.total - loan.total_amount_paid), 
        "receipt_number" : payment.receipt_number
    })

@api_view(["POST"])
def get_payment_by_search(request): 
    name = request.data.get("name")
    sort = request.data.get("sort")
    order = request.data.get("order")
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")
    pagination = request.data.get("pagination")
    limit = request.data.get("limit")

    if not sort : 
        sort = "date"

    if not order : 
        order = "asc"

    if not limit : 
        limit = 25

    conditions = Q()

    if name : 
        conditions &= Q(loan__client__full_name__icontains = name.strip())

    if start_date : 
        converted_start_date = parse_date(start_date)

        if converted_start_date :
            conditions &= Q(date__gte = start_date)

    if end_date : 
        converted_end_date = parse_date(end_date)

        if converted_end_date :
            conditions &= Q(date__lte = end_date)

    if not start_date and not end_date :
        conditions &= Q(date = timezone.now().date())

    if order == "asc" :

        if sort == "date" : 
            order_by = ["date" , "time"]

        elif sort == "amount" : 
            order_by = ["amount"]

        elif sort == "name" :
            order_by = ["loan__client__full_name"]

    elif order == "desc" : 

        if sort == "date" : 
            order_by = ["-date" , "-time"]

        elif sort == "amount" : 
            order_by = ["-amount"]

        elif sort == "name" :
            order_by = ["-loan__client__full_name"]

    payments = Payment.objects.filter(conditions).order_by(*order_by)

    total_count = payments.count()
    total_page = total_count/limit

    if total_page % 1 != 0:
        total_page = math.floor(total_page)
        total_page += 1

    if total_page == 0:
        total_page = 1

    if pagination :
        included = int(pagination) * limit

    else :
        pagination = 1 
        included = limit

    response = []

    i = 1 
    number_display = 1 + ((int(pagination) -1) * limit)

    for payment in payments : 

        if i <= included :
            data = {
                "id": payment.id,
                "number_display": number_display,
                "receipt_number" : payment.receipt_number if payment.receipt_number else "None",
                "payment_amount": format_number_with_commas(payment.amount) if payment.amount else "None", 
                "date": payment.date.strftime("%m-%d-%Y"),
                "time": payment.time.strftime("%I:%M:%S %p") if payment.time else "None",  
                "client_name" : payment.loan.client.full_name
            }

            number_display += 1

            response.append(data)

        i += 1

    if not start_date and not end_date : 
        date_range_marker = "Showing payments for today"

    elif start_date and converted_start_date and not end_date :
        date_range_marker = "Showing payments from " + start_date + " to today"

    elif not start_date and end_date and converted_end_date :
        date_range_marker = "Showing payments before " + end_date

    elif converted_start_date and converted_end_date and start_date and end_date :
        date_range_marker = "Showing payments from " + start_date + " to " + end_date


    return Response({
        "status": 1,
        "status_message": "Payments retrieved successfully",
        "payments": response,
        "pagination" : pagination,
        "total_page" : total_page, 
        "date_range_marker" : date_range_marker
    })



@api_view(["GET"])
def get_payment_table(request):

    result = []
    for i in range(6, -1, -1):
        days_ago = timezone.now() - datetime.timedelta(days=i)
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