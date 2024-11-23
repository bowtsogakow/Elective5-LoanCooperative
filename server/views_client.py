from .models import ClientInfo, Loan, User
from rest_framework.response import Response
from rest_framework.decorators import api_view



# Not yet Tested
@api_view(["POST"])
def add_client(request): 
    first_name = request.data.get("first_name")
    middle_name = request.data.get("middle_name")
    last_name = request.data.get("last_name")
    address = request.data.get("address")
    contact_no = request.data.get("contact_no")
    work_details = request.data.get("work_details")
    business = request.data.get("business")
    co_maker = request.data.get("co_maker")
    billing_statement_electric = request.Files.get("billing_statement_electric")
    billing_statement_water = request.Files.get("billing_statement_water")
    type = "client"

    if not first_name or not last_name or not middle_name or not address or not contact_no or not work_details or not business or not co_maker or not billing_statement_electric or not billing_statement_water:
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
    
        user = User.objects.create(
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            type = type
        )

        co_maker_object = User.objects.filter(first_name = co_maker.split(" ")[0], middle_name = co_maker.split(" ")[1], last_name = co_maker.split(" ")[2], type = "client").first()
        if user and co_maker_object: 

            client = ClientInfo.objects.create(
                user = user,
                address = address,
                contact_no = contact_no,
                work_details = work_details,
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

    return Response({
        "status" : 1,
        "status_message" : "Client added successfully",
        "client_id" : client.id 
    })


@api_view(["GET"])
def get_all_clients(request): 
    
    clients = User.objects.filter(type = "client")

    response_json = []
    
    for client in clients : 
        client = ClientInfo.objects.filter(user = client).first()

        if not client : 
            continue
        
        hasLoan = False
        loan = Loan.objects.filter(client = client).first()
        if loan : 
            if loan.status == "ongoing" :
                hasLoan = True
        
        data = {
            "id" : client.id,
            "fullname" : client.full_name,
            "contact_number" : client.contact_no,
            "address" : client.address, 
            "has_loan" : hasLoan
        } 

        response_json.append(data)

    return Response({
        "status" : 1,
        "status_message" : "Success",
        "clients" : response_json
    })

@api_view(["GET"])
def get_client_by_id(request, client_id):
    client = User.objects.filter(id = client_id, type = "client").first()

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
            "id" : clientInfo.id,
            "fullname" : clientInfo.full_name,
            "contact_number" : clientInfo.contact_no,
            "address" : clientInfo.address, 
            "work_details" : clientInfo.work_details,
            "business" : clientInfo.business,
            "co_maker" : clientInfo.co_maker.full_name,
            "billing_statement_electric" : clientInfo.billing_statement_electric.url,
            "billing_statement_water" : clientInfo.billing_statement_water.url
        } 

        return Response({
            "status" : 1,
            "status_message" : "Success",
            "client" : data
        })