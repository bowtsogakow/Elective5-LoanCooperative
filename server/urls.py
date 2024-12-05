from django.urls import path
from server import views_loan, views_client, views_auth
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # authentication 
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),

    # client
    path("add_client", views_client.add_client, name="server_add_client"),
    path("get_all_clients", views_client.get_all_clients, name="server_get_all_clients"),
    path("get_client_by_id/<int:client_id>", views_client.get_client_by_id, name="server_get_client_by_id"),
    
    # loans
    path("add_loan", views_loan.add_loan, name="server_add_loan"),
    path("get_all_loans", views_loan.get_all_loans, name="server_get_all_loans"),
    path("get_loan_by_id/<int:loan_id>", views_loan.get_loan_by_id, name="server_get_loan_by_id"),
]