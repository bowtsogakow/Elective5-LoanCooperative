import math
from .models import ClientInfo, Loan, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(["GET"])
def get_all_employees(request):
    employees = User.objects.filter(type = "cashier" or "admin")

    response_json = []
    
    for employee in employees : 

        if not employee : 
            continue
        
        
        data = {
           "id" : employee.id,
            "username" : employee.username,
            "email" : employee.email,
            "first_name" : employee.first_name,
            "middle_name" : employee.middle_name,
            "last_name" : employee.last_name,
            "fullname" : employee.full_name,
            "type" : employee.type,
        } 

        response_json.append(data)

    return Response({
        "status" : 1,
        "status_message" : "Employees retrieved successfully",
        "employees" : response_json
    })

@api_view(["GET"])
def get_employee_by_id(request, employee_id):
    employee = User.objects.filter(id = employee_id).first()

    if not employee : 
        return Response({
            "status" : 0,
            "status_message" : "Employee not found"
        })

    data = {
        "id" : employee.id,
        "username" : employee.username,
        "email" : employee.email,
        "first_name" : employee.first_name,
        "middle_name" : employee.middle_name,
        "last_name" : employee.last_name,
        "fullname" : employee.full_name,
        "type" : employee.type,
    } 

    return Response({
        "status" : 1,
        "status_message" : "Employee retrieved successfully",
        "employee" : data
    })

@api_view(["POST"])
def add_employee(request): 
    email = request.data.get("email")
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    middle_name = request.data.get("middle_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")
    type = request.data.get("type")


    if not (email and username and first_name and middle_name and last_name and password and type):
        return Response({
            "status" : 0,
            "status_message" : "Invalid input"
        })
    
    employee = User.objects.filter(first_name=first_name, middle_name=middle_name, last_name=last_name, type = type).first()

    if employee : 
        return Response({
            "status" : 0,
            "status_message" : "User already exist"
        })
    
    try : 

        new_employee = User(
            email = email, 
            username = username, 
            first_name = first_name, 
            middle_name = middle_name,
            last_name = last_name,
            password = password,
            type = type
        )

        new_employee.save()

        return Response({
            "status" : 1, 
            "status_message" : "User created successfully"
        })

    except Exception as e : 
        return Response({
            "status" : 0, 
            "status_message" : f"Error in creating employee : {str(e)}"
        })
    
@api_view(["POST"])
def delete_employee(request):
    ids = request.data.get("employee_ids")

    if type(ids) is not list :
        return Response({
            "status" : 0,
            "status_message" : "Invalid input"
        })
    
    for id in ids :
        employee = User.objects.filter(id = id, type = "cashier" or "admin").first()
        if not employee: 
            continue
        
        employee.delete()
     

    return Response({
        "status" : 1,
        "status_message" : "Clients deleted successfully"
    })

@api_view(["POST"])
def get_employee_by_search(request):
    name = request.data.get("name", None)
    type = request.data.get("type")
    pagination = request.data.get("pagination")
    limit = 25

    if not type and not (type == "admin" or type == "cashier" or type == "all"): 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid Input"
        })
    
    
    conditions = Q()

    conditions &= Q(is_active = True)
    
    if name : 
        conditions &= Q(full_name__icontains = name.strip())

    if type == "cashier" or type == "admin":
        print(type)
        conditions &= Q(type = type)

    elif type == "all":
        conditions &= ~Q(type = "client")

    employees = User.objects.filter(conditions)

    total_count = employees.count()
    total_page = total_count/limit

    if total_page % 1 != 0:
        total_page = math.floor(total_page)
        total_page += 1

    if pagination :
        included = int(pagination) * limit

    else :
        pagination = 1 
        included = limit

    response = []

    i = 1 
    number_display = 1
    for employee in employees :
        if  included - limit < i <= included :
        
            data = {
                "id" : employee.id,
                "number_display" : number_display,
                "fullname" : employee.full_name,
                "email" : employee.email,
                "username" : employee.username,
                "type" : employee.type
            }
            number_display += 1 
            response.append(data)

        i += 1


    return Response({
        "status" : 1,
        "status_message" : "Employees retrieved successfully",
        "employees" : response,
        "pagination" : pagination,
        "total_page" : total_page
    })
