from .models import ClientInfo, Loan, User
from rest_framework.response import Response
from rest_framework.decorators import api_view

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