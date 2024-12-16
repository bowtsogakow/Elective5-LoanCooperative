from .models import ClientInfo, Loan, Payment, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
import math
from django.utils import timezone
import datetime


# Not yet Tested
@api_view(["POST"])
def add_client(request): 
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    middle_name = request.data.get("middle_name")
    last_name = request.data.get("last_name")
    address = request.data.get("address")
    contact_no = request.data.get("contact_no")
    business = request.data.get("business")
    co_maker = request.data.get("co_maker")
    billing_statement_electric = request.FILES.get("billing_statement_electric")
    billing_statement_water = request.FILES.get("billing_statement_water")
    type = "client"

    user = None 
    client = None 

    if not email or not username or not password or not first_name or not last_name or not middle_name or not address or not contact_no or not business or not co_maker or not billing_statement_electric or not billing_statement_water:
        return Response({
            "status" : 0,
            "status_message" : "Missing invalid input"
        })

    user = User.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name, type = type).first()

    if user : 
        return Response({
            "status" : 0,
            "status_message" : "Client already exist"
        })
    
    try : 
    
        user = User(
            email = email,
            username = username,
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            type = type
        )

        user.set_password(password)

        co_maker_object = User.objects.filter(full_name = co_maker).first()
        print(co_maker_object)
        if user and co_maker_object: 

            client = ClientInfo(
                user = user,
                address = address,
                contact_no = contact_no,
                business = business,
                co_maker = co_maker_object,
                billing_statement_electric = billing_statement_electric,
                billing_statement_water = billing_statement_water,
            )

        else : 
            return Response({
                "status" : 0,
                "status_message" : "Something went wrong"
            })

    except Exception as e : 
        if user : 
            user.delete()
        
        if client : 
            client.delete()
        return Response({
            "status" : 0,
            "status_message" : "Something went wrong"
        })

    print(7)    
    user.save()
    client.save()

    
    return Response({
        "status" : 1,
        "status_message" : "Client added successfully",
        "client_id" : client.id 
    })

@api_view(["GET"])
def get_all_clients(request): 
    
    clients = User.objects.filter(type = "client", is_active = True)

    response_json = []
    
    for client in clients : 

        if not client : 
            continue
        
        info = ClientInfo.objects.filter(user = client).first()

        if not info : 
            continue
        
        data = {
            "id" : client.id,
            "fullname" : client.full_name,
            "contact_number" : info.contact_no,
            "address" : info.address, 
            "has_loan" : client.has_loan
        } 

        response_json.append(data)

    return Response({
        "status" : 1,
        "status_message" : "Success",
        "clients" : response_json
    })

@api_view(["GET"])
def get_client_by_id(request, client_id):
    print(client_id)
    client = User.objects.filter(id = client_id, type = "client", is_active = True).first()

    if not client : 
        return Response({
            "status" : 0,
            "status_message" : "Client does not exist"
        })

    if client:
        clientInfo = ClientInfo.objects.filter(user = client).first()

        if not clientInfo :
            return Response({
                "status" : 0,
                "status_message" : "Missing information on client"
            })
        
        data = {
            "id" : client.id,
            "fullname" : client.full_name,
            "contact_number" : clientInfo.contact_no,
            "has_loan" : client.has_loan,
            "address" : clientInfo.address, 
            "business" : clientInfo.business,
            "co_maker" : clientInfo.co_maker.full_name if clientInfo.co_maker else None,
            "billing_statement_electric" : clientInfo.billing_statement_electric.url,
            "billing_statement_water" : clientInfo.billing_statement_water.url
        } 

        return Response({
            "status" : 1,
            "status_message" : "Success",
            "client" : data
        })
    
@api_view(["POST"])
def get_clients_by_search(request):
    name = request.data.get("name", None)
    loan_status = request.data.get("loan_status")
    pagination = request.data.get("pagination")
    limit = 25

    if not loan_status: 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid Input"
        })
    
    
    conditions = Q()

    conditions &= Q(type = "client", is_active = True)
    
    if name : 
        conditions &= Q(full_name__icontains = name.strip())

    if loan_status == "has-loan": 
        conditions &= Q(has_loan = True)
    
    elif loan_status == "has-no-loan": 
        conditions &= Q(has_loan = False) 

    clients = User.objects.filter(conditions).prefetch_related("ClientInfos")
    total_count = clients.count()
    total_page = total_count/limit

    if total_page % 1 != 0:
        total_page = math.floor(total_page)
        total_page += 1

    if pagination :
        included = int(pagination) * limit

    else :
        pagination = 1 
        included = limit
    
    print(type(included))
    print(type(pagination))

    response = []

    i = 1 
    number_display = 1
    for client in clients :
        if  included - limit < i <= included :
        
            clientInfo = client.ClientInfos.first()

            if not clientInfo : 
                continue

            data = {
                "id" : client.id,
                "number_display" : number_display,
                "fullname" : client.full_name,
                "contact_number" : clientInfo.contact_no,
                "address" : clientInfo.address, 
                "has_loan" : client.has_loan
            }
            number_display += 1 
            response.append(data)

        i += 1

    return Response({
        "status" : 1,
        "status_message" : "Success",
        "clients" : response,
        "pagination" : pagination,
        "total_page" : total_page
    })

@api_view(["POST"])
def delete_client(request) :
    ids = request.data.get("client_ids")

    if type(ids) is not list :
        return Response({
            "status" : 0,
            "status_message" : "Invalid input"
        })
    
    for id in ids :
        client = User.objects.filter(id = id, type = "client").prefetch_related("ClientInfos").first()
        
        if not client :
            continue
            
        client.ClientInfos.first().delete()
        client.delete()

    return Response({
        "status" : 1,
        "status_message" : "Clients deleted successfully"
    })


@api_view(["GET"])
def get_eligible_clients_for_loan(request): 
    clients = User.objects.filter(type = "client", has_loan = False).prefetch_related("ClientInfos")

    response = []

    for client in clients : 
        clientInfo = client.ClientInfos.first()

        if not clientInfo : 
            continue

        if not clientInfo.billing_statement_electric or not clientInfo.billing_statement_water :
            continue

        if not clientInfo.co_maker : 
            continue

        data = {
            "id" : client.id,
            "fullname" : client.full_name,
        } 

        response.append(data)

    sorted_response = sorted(response, key = lambda x : x["fullname"])

    return Response({
        "status" : 1,
        "status_message" : "Eligible clients were retrieved successfully",
        "clients" : sorted_response
    })


@api_view(["GET"])
def get_client_registration_table(request):

    result = []
    for i in range(6, -1, -1):
        days_ago = timezone.now() - datetime.timedelta(days=i)
       
        clients = User.objects.filter(type = "client", is_active = True, date_joined__date=days_ago).count()

        result.append({
            "date" : days_ago.strftime('%Y-%m-%d'),
            "client_count" : clients
        })

        
    return Response({
        "status" : 0, 
        "status_message" : "Success",
        "result" : result
    })