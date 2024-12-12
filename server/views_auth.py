from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["POST"])
def server_login(request):

    username = request.data.get("username")
    password = request.data.get("password") 
    type = request.data.get("type")
    http_request = request._request

    if not username or not password or not type: 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid input"
        })
     
    user = authenticate(request, username=username, password=password)
    print(user.type)
    print(type)

    if not user : 
        return Response({
            "status" : 0, 
            "status_message" : "Invalid credentials"
        })
    
    if type == "admin" and user.type == "admin" : 
        login(http_request, user)
        # redirect('admin_index')
        return Response({
            "status" : 1, 
            "status_message" : "Logged in as admin"
        })
    
    if type == "cashier" and user.type == "cashier" : 
        login(http_request, user)
        return Response({
            "status" : 1, 
            "status_message" : "Logged in as cashier"
        })
    
    
    if type == "client" and user.type == "client" : 
        login(http_request, user)
        return Response({
            "status" : 1, 
            "status_message" : "Logged in as client"
        })

    return Response({
        "status" : 0, 
        "status_message" : "Failed to login user"
    })
    
              