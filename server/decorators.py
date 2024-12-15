from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

# Currently says no permission kahit anong account type
# - which means that if you are an unauthenticated admin, lalabas yung no permission, instead of login button 
# - no permission/forbidden should only appear if you are authenticated and you access something instead 
#       - eg. (logged in as client and accesses /admin/ pages)

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_page")
        if request.user.is_authenticated and request.user.type == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view


def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_page")
        if request.user.is_authenticated and request.user.type == 'client':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view

def cashier_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_page")
        if request.user.is_authenticated and request.user.type == 'cashier':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view