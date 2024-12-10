from django.urls import path
from server import views_loan, views_client, views_payment, views_auth, views_employees
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # authentication 
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),

    # client
    path("add_client", views_client.add_client, name="server_add_client"),
    path("get_all_clients", views_client.get_all_clients, name="server_get_all_clients"),
    path("get_client_by_id/<int:client_id>", views_client.get_client_by_id, name="server_get_client_by_id"),
    path("get_client_by_search", views_client.get_clients_by_search, name="server_get_client_by_search"),
    path("delete_client", views_client.delete_client, name="server_delete_client"),
    
    # loans
    path("add_loan", views_loan.add_loan, name="server_add_loan"),
    path("get_all_loans", views_loan.get_all_loans, name="server_get_all_loans"),
    path("get_loan_by_id/<int:loan_id>", views_loan.get_loan_by_id, name="server_get_loan_by_id"),
    path("get_loan_list_by_client/<int:client_id>", views_loan.get_loan_list_by_client, name="server_get_loan_list_by_client"),

    # payment
    # path("add_payment/<int:loan_id>", views_loan.add_payment, name="server_add_payment"),
    # path("get_payment_by_id/<int:payment_id>", views_loan.get_payment_by_id, name="server_get_payment_by_id"),
    path("get_payment_list_by_loan/<int:loan_id>", views_payment.get_payment_list_by_loan, name="server_get_payment_list_by_loan"),
    path("get_payment_list_by_client/<int:client_id>", views_payment.get_payment_list_by_client, name="server_get_payment_list_by_client"),

    #employee
    path("get_all_employees", views_employees.get_all_employees, name="server_get_all_employees"),
]