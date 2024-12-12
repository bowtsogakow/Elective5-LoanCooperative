from django.urls import path
from auth_frontend import views 

urlpatterns = [
    path("", views.login_page, name = "login_page")
]