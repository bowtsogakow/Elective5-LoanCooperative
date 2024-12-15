from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout

@api_view(["POST"])
def server_login(request):

    username = request.data.get("username")
    password = request.data.get("password") 
    type = request.data.get("type")
    http_request = request._request

    print(username, password, type)

    if not username or not password or not type: 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid input"
        })
     
    user = authenticate(request, username=username, password=password)
    
    if not user : 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid credentials"
        })
    
    if type == "client" and user.type == "client" : 
        login(http_request, user)
        return Response({
            "status" : 1, 
            "status_message" : "Logged in as client",
            "client_id" : user.id
        })

    
    if type == "cashier" and user.type == "cashier" : 
        login(http_request, user)
        return Response({
            "status" : 2, 
            "status_message" : "Logged in as cashier"
        })
    
    if type == "admin" and user.type == "admin" : 
        login(http_request, user)
        return Response({
            "status" : 3, 
            "status_message" : "Logged in as admin"
        })

    return Response({
        "status" : 0, 
        "status_message" : "Failed to login user"
    })
    
def server_logout(request):
    logout(request)  # Log the user out
    return redirect('login_page')