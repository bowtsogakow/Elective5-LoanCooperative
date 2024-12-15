from django.urls import path
from server import views_loan, views_client, views_payment, views_auth, views_employees
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # authentication 
    path("login", views_auth.server_login, name="server_login"),
    

    # client
    path("add_client", views_client.add_client, name="server_add_client"),
    path("get_all_clients", views_client.get_all_clients, name="server_get_all_clients"),
    path("get_client_by_id/<int:client_id>", views_client.get_client_by_id, name="server_get_client_by_id"),
    path("get_client_by_search", views_client.get_clients_by_search, name="server_get_client_by_search"),
    path("delete_client", views_client.delete_client, name="server_delete_client"),
    path("get_eligible_clients_for_loan", views_client.get_eligible_clients_for_loan, name="server_get_eligible_clients_for_loan"),
    # loans
    path("add_loan", views_loan.add_loan, name="server_add_loan"),
    path("get_all_loans", views_loan.get_all_loans, name="server_get_all_loans"),
    path("get_loan_by_id/<int:loan_id>", views_loan.get_loan_by_id, name="server_get_loan_by_id"),
    path("get_loan_list_by_client/<int:client_id>", views_loan.get_loan_list_by_client, name="server_get_loan_list_by_client"),
    path("get_loan_by_code", views_loan.get_loan_by_code, name="server_get_loan_by_code"),
    path("get_loans_by_search", views_loan.get_loans_by_search, name="server_get_loans_by_search"),

    # payment
    path("add_payment", views_payment.add_payment, name="server_add_payment"),
    # path("get_payment_by_id/<int:payment_id>", views_loan.get_payment_by_id, name="server_get_payment_by_id"),
    path("get_payment_list_by_loan/<int:loan_id>", views_payment.get_payment_list_by_loan, name="server_get_payment_list_by_loan"),
    path("get_payment_list_by_client/<int:client_id>", views_payment.get_payment_list_by_client, name="server_get_payment_list_by_client"),

    #employee
    path("get_all_employees", views_employees.get_all_employees, name="server_get_all_employees"),
    path("add_employee", views_employees.add_employee, name = "server_add_employee"),
    path("get_employee_by_search", views_employees.get_employee_by_search, name="server_get_employee_by_search"),
    path("delete_employee", views_employees.delete_employee, name="server_delete_employee"),
    path("get_employee_by_id/<int:employee_id>", views_employees.get_employee_by_id, name="server_get_employee_by_id"),
    path("update_employee", views_employees.update_employee, name="server_update_employee"),
    path("update_employee_password", views_employees.update_employee_password, name="server_update_employee_password"),
    path("change_employee_position", views_employees.change_employee_position, name="server_change_employee_position"),
]