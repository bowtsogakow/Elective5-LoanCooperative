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