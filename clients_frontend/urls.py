from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="client_index"),
    path("profile", views.profile_page, name="client_profile"),
]