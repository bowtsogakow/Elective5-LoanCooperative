import datetime
import math
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from server.models import ClientInfo, Loan, User
from django.db.models import F
from .utils import format_number_with_commas


@api_view(["POST"])
def add_loan(request): 
    client_name = request.data.get("client_name")
    loan_term = request.data.get("loan_term")
    amount_loaned = request.data.get("amount_loaned")
    interest_percentage = request.data.get("interest_percentage")
    interest_mode = request.data.get("interest_mode")
    type = "loan"

    if not client_name or not loan_term or not amount_loaned or not interest_percentage or not interest_mode:
        return Response({
            "status" : 0,
            "status_message" : "Missing invalid input"
        })

    client = User.objects.filter(full_name = client_name, type = "client").first()
    clientInfo = ClientInfo.objects.filter(user = client).first()

    if not client : 
        return Response({
            "status" : 0,
            "status_message" : "Client does not exist"
        })
    
    if not clientInfo.co_maker or not clientInfo.billing_statement_electric or not clientInfo.billing_statement_water :
        return Response({
            "status" : 0,
            "status_message" : "Please ensure that client had already completed their requirements"
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
        payment_position = loan.days_paid - days_passed

        data = {
            "id" : loan.id,
            "client_name" : loan.client.full_name,
            "amount_loaned" : loan.amount_loaned, 
            "total_amount" : loan.total,
            "status" : loan.status, 
            "remaining_balance" : loan.total - loan.total_amount_paid,  
            "start_date" : loan.date_created,
            "end_date" : loan.date_end,
            "daily_payment" : loan.daily_payment, 
            "days_left" : loan.days_total - loan.days_paid, 
            "payment_position" : payment_position, 

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
        "amount_loaned" : format_number_with_commas(loan.amount_loaned), 
        "interest_percentage" : loan.interest_percentage,
        "loan_term" : loan.loan_term,
        "interest_mode" : loan.interest_mode,
        "interest" : format_number_with_commas(loan.interest),
        "total" : format_number_with_commas(loan.total),
        "days_total" : loan.days_total,
        "days_paid" : loan.days_paid,
        "total_amount_paid" : format_number_with_commas(loan.total_amount_paid),
        "remaining_balance" : format_number_with_commas(loan.total - loan.total_amount_paid),
        "payment_progress_percentage" : ((loan.total_amount_paid) / loan.total) * 100,
        "status" : loan.status, 
        "date_created" : loan.date_created,
        "date_end" : loan.date_end,
        "daily_payment" : format_number_with_commas(loan.daily_payment), 
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
            "amount" : format_number_with_commas(loan.amount_loaned), 
            "interest_percentage" : loan.interest_percentage,
            "loan_term" : loan.loan_term,
            "total" : format_number_with_commas(loan.total),
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
    
    loan = Loan.objects.filter(qr_code = qr_code, status = "ongoing").first()

    if not loan : 
        return Response({
            "status" : 0,
            "status_message" : "Loan does not exist"
        })

    data = {
        "id" : loan.id,
        "client_name" : loan.client.full_name,
        "daily_payment" : format_number_with_commas(loan.daily_payment),
        "remaining_balance" : format_number_with_commas(loan.total - loan.total_amount_paid),
    }

    return Response({
        "status" : 1,   
        "status_message" : "Loan retrieved successfully",
        "loan" : data
    })


@api_view(["POST"])
def get_loans_by_search(request):
    name = request.data.get("name")
    sort = request.data.get("sort")
    order = request.data.get("order")
    status = request.data.get("status")
    pagination = request.data.get("pagination")
    limit = 25

    if not sort : 
        sort = "client_name"

    if not order: 
        order = "asc"

    if not status : 
        status = "all"

    conditions = Q()

    if name: 
        conditions &= Q(client__full_name__icontains = name.strip())

    if status == "ongoing":
        conditions &= Q(status = "ongoing")

    elif status == "completed":
        conditions &= Q(status = "completed")

    if order == "asc" : 

        if sort == "client_name":
            order_by = "client__full_name"
        
        elif sort == "amount_loaned": 
            order_by = "amount_loaned"

        elif sort == "total_amount":
            order_by = "total"

        elif sort == "start_date": 
            order_by = "date_created"

        elif sort == "end_date": 
            order_by = "date_end"

        elif sort == "daily_payment": 
            order_by = "daily_payment"

        elif sort == "days_left": 
            order_by = "days_total"

        elif sort == "payment_position":
            current_date = datetime.date.today()
            order_by = F('days_paid') - (current_date - F('date_created'))

    elif order == "desc" : 

        if sort == "client_name":
            order_by = "-client__full_name"
        
        elif sort == "amount_loaned": 
            order_by = "-amount_loaned"

        elif sort == "total_amount":
            order_by = "-total"

        elif sort == "start_date": 
            order_by = "-date_created"

        elif sort == "end_date": 
            order_by = "-date_end"

        elif sort == "daily_payment": 
            order_by = "-daily_payment"

        elif sort == "days_left": 
            order_by = "-days_total"

        elif sort == "payment_position":
            current_date = datetime.date.today()
            order_by = (current_date - F('date_created')) - F('days_paid')

      
    loans = Loan.objects.filter(conditions).order_by(order_by)

    total_count = loans.count()
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
    number_display = 1 + ( (int(pagination) - 1) * limit)

    for loan in loans : 
        if included - limit < i <= included :

            
            days_passed = (datetime.date.today() - loan.date_created).days
            payment_position = loan.days_paid - days_passed

            data = {
                "id" : loan.id,
                "number_display" : number_display,
                "client_name" : loan.client.full_name,
                "amount_loaned" : format_number_with_commas(loan.amount_loaned), 
                "total_amount" : format_number_with_commas(loan.total),
                "status" : loan.status, 
                "remaining_balance" : format_number_with_commas(loan.total - loan.total_amount_paid),  
                "start_date" : loan.date_created.strftime("%m-%d-%Y"),
                "end_date" : loan.date_end.strftime("%m-%d-%Y"),
                "daily_payment" : format_number_with_commas(loan.daily_payment), 
                "days_left" : loan.days_total - loan.days_paid, 
                "payment_position" : payment_position, 

            }
            number_display += 1
            response.append(data)

        i += 1

    return Response({
        "status" : 1,   
        "status_message" : "Loans retrieved successfully",
        "loans" : response,
        "pagination" : pagination,
        "total_page" : total_page,
    })


@api_view(["GET"])
def get_latest_loan_by_client(request, client_id):
    client = User.objects.filter(id = client_id).first()

    if not client: 
        return Response({
            "status" : 0,
            "status_message" : "Client does not exist"
        })

    loan = Loan.objects.filter(client = client, status = "ongoing").order_by("-date_created").first()

    if not loan : 
        return Response({
            "status" : 2,
            "status_message" : "Client does not have any existing loan"
        })
    
    remaining_balance = loan.total - loan.total_amount_paid
    progress = loan.total - remaining_balance / loan.total
    progress *= 100

    data = {
        "id" : loan.id,
        "client_name" : loan.client.full_name,
        "amount_loaned" : format_number_with_commas(loan.amount_loaned),   
        "total_amount" : format_number_with_commas(loan.total),
        "interest_percentage" : loan.interest_percentage,   
        "status" : loan.status,
        "remaining_balance" : format_number_with_commas(remaining_balance),
        "loan_term" : loan.loan_term,
        "start_date" : loan.date_created,
        "end_date" : loan.date_end,
        "days_left" : loan.days_total - loan.days_paid,
        "payment_position" : loan.days_paid - (datetime.date.today() - loan.date_created).days,
        "daily_payment" : format_number_with_commas(loan.daily_payment),
        "interest" : format_number_with_commas(loan.interest),
        "qr_code" : loan.qr_code, 
        "progress" : progress
    }

    return Response({
        "status" : 1,
        "status_message" : "Loan retrieved successfully",
        "loan" : data
    })
    

    