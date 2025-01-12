import datetime
import math
from .models import ClientInfo, Loan, Payment, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Sum
from .utils import format_number_with_commas

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
            type = type
        )

        new_employee.set_password(password) 

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
        print(id)
        employee = User.objects.filter(id = id).first()
        if not employee: 
            print("Not exist")
            continue
        
        employee.delete()
     

    return Response({
        "status" : 1,
        "status_message" : "Employees has been deleted successfully"
    })

@api_view(["POST"])
def get_employee_by_search(request):
    
    id = request.data.get("id")
    str_id = str(id)
    name = request.data.get("name")
    type = request.data.get("type")
    pagination = request.data.get("pagination")
    permission = request.data.get("permission")
    order = request.data.get("order")
    limit = 25

    if not type and not (type == "admin" or type == "cashier" or type == "all"): 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid Input"
        })
    
    if not order : 
        order = "asc"
    
    conditions = Q()

    conditions &= Q(is_active = True)
    
    if name : 
        conditions &= Q(full_name__icontains = name.strip())

    if type == "cashier" or type == "admin":
        print(type)
        conditions &= Q(type = type)

    elif type == "all":
        conditions &= ~Q(type = "client")

    if order == "asc":
        order_by = "full_name"

    elif order == "desc":
        order_by = "-full_name"


    employees = User.objects.filter(conditions).order_by(order_by)

    total_count = employees.count() - 1
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
    number_display = 1 + (( int(pagination) - 1 ) * limit) 
    for employee in employees :
        if  included - limit < i <= included :
        
            if employee.type == "admin" and permission != "superadmin" : 
                continue
            
            str_emp_id = str(employee.id)
            if str_emp_id == str_id : 
                continue
            
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


@api_view(["POST"])
def update_employee(request):
    id = request.data.get("id")
    email = request.data.get("email") 
    username = request.data.get("username") 
    first_name = request.data.get("first_name") 
    middle_name = request.data.get("middle_name") 
    last_name = request.data.get("last_name")

    if not id: 
        return Response({
            "status" : 0,  
            "status_message" : "Invalid input"
        })
    
    employee = User.objects.filter(id = id).first()

    if not employee : 
        return Response({
            "status" : 0, 
            "status_message" : "Employee does not exist"
        })
    
    try : 

        if email : 
            employee.email = email.strip()
        
        if username : 
            employee.username = username.strip()
        
        if first_name : 
            employee.first_name = first_name.strip()
            
        if middle_name:    
            employee.middle_name = middle_name.strip()
            
        if last_name:     
            employee.last_name = last_name.strip()

        employee.save()

        return Response({
            "status" : 1,
            "status_message" : "Employee updated successfully"
        })

    except Exception as e : 
        return Response({
            "status" : 0,
            "status_message" : f"Error in updating employee : {str(e)}"
        })
    

@api_view(["POST"])
def update_employee_password(request):
    id = request.data.get("id")
    new_password = request.data.get("new_password")
    old_password = request.data.get("old_password")

    if not id: 
        return Response({
            "status" : 0,  
            "status_message" : "Invalid input"
        })
    
    employee = User.objects.filter(id = id).first()

    if not employee : 
        return Response({
            "status" : 0, 
            "status_message" : "Employee does not exist"
        })
    
    try : 

        if employee.check_password(old_password.strip()) == False : 
            return Response({
                "status" : 0,
                "status_message" : "Old password is incorrect"
            })

        employee.set_password(new_password.strip())
        employee.save()

        return Response({
            "status" : 1,
            "status_message" : "Password updated successfully"
        })
    
    except Exception as e : 
        return Response({
            "status" : 0,
            "status_message" : f"Error in updating password : {str(e)}"
        })
    

@api_view(["POST"])
def change_employee_position(request):
    id = request.data.get("id")
    type = request.data.get("type")

    if not id: 
        return Response({
            "status" : 0,  
            "status_message" : "Invalid input"
        })
    
    employee = User.objects.filter(id = id).first()

    if not employee : 
        return Response({
            "status" : 0, 
            "status_message" : "Employee does not exist"
        })
    
    try : 
        print(type)
        if employee.type == type : 
            return Response({
                "status" : 1,
                "status_message" : f"{employee.full_name} already has this position",
                "type" : employee.type
            })
        
        employee.type = type
        employee.save()

        return Response({
            "status" : 1,
            "status_message" : f"{employee.full_name} position has been change to {employee.type}",
            "type" : employee.type
        })
    
    except Exception as e : 
        return Response({
            "status" : 0,
            "status_message" : f"Error in updating position : {str(e)}"
        })
 
@api_view(["GET"])
def get_dashboard_info(request): 
    
    clients = User.objects.filter(type = "client", is_active = True).count()
    clients_added_in_the_current_month = User.objects.filter(type = "client", is_active = True, date_joined__month = datetime.datetime.now().month).count()
    clients_change_label = f"+{clients_added_in_the_current_month} in the current month"

    total_loaned_amount = Loan.objects.filter(status = "ongoing").aggregate(total = Sum('amount_loaned'))
    first_day_of_month = datetime.date.today().replace(day=1)
    last_month_loaned_amount = Loan.objects.filter(status = "ongoing", date_created__lte = first_day_of_month).aggregate(total = Sum('amount_loaned'))
    
    if last_month_loaned_amount["total"] and total_loaned_amount["total"]:
        percentage_increase = ( (total_loaned_amount["total"] - last_month_loaned_amount["total"]) / last_month_loaned_amount["total"] ) * 100
        loan_change_label = f"+ {round(percentage_increase, 2)}% from last month"

    elif last_month_loaned_amount["total"] and not ["total"]:
        loan_change_label = f"-100% from last month"

    elif not last_month_loaned_amount["total"] and total_loaned_amount["total"]:
        loan_change_label = f"+100% from last month"

    else : 
        loan_change_label = f"+0% from last month"
        
    formatted_loaned_amount = format_number_with_commas(total_loaned_amount["total"])

    today = datetime.date.today()
    total_payments = Payment.objects.filter(date = today).aggregate(total = Sum('amount'))
    yesterday_payments = Payment.objects.filter(date = today - datetime.timedelta(days=1)).aggregate(total = Sum('amount'))
    formatted_total_payments = format_number_with_commas(total_payments["total"])

    if yesterday_payments["total"] and total_payments["total"]:
        print(yesterday_payments["total"], total_payments["total"])
        percentage_increase = ( (total_payments["total"] - yesterday_payments["total"]) / yesterday_payments["total"] ) * 100
        payments_change_label = f"+{round(percentage_increase, 2)}% from yesterday"

    elif yesterday_payments["total"] and not ["total"]:
        payments_change_label = f"-100% from yesterday"

    elif not yesterday_payments["total"] and total_payments["total"]:
        payments_change_label = f"+100% from yesterday"

    else : 
        payments_change_label = f"+0% from yesterday"


    return Response({
        "status" : 1,
        "status_message" : "Dashboard info retrieved successfully",
        "clients" : clients,
        "clients_change_label" : clients_change_label, 
        "total_loaned_amount" : formatted_loaned_amount, 
        "loan_change_label" : loan_change_label,   
        "total_payments" : formatted_total_payments, 
        "payments_change_label" : payments_change_label
    })