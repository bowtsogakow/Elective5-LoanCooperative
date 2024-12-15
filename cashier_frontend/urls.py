from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="cashier_index"),
    path("profile/<int:id>", views.profile_page, name = "cashier_profile_info"),
]