# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    username = data.get("userName")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"message": "userName and password required"}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)

    return JsonResponse({"userName": username, "status": "Failed"}, status=401)


@csrf_exempt
def logout_user(request):
    # React bazı şablonlarda GET, bazılarında POST atıyor
    if request.method not in ["GET", "POST"]:
        return JsonResponse({"message": "GET/POST required"}, status=405)

    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out"}, status=200)

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    userName = data.get("userName")
    password = data.get("password")
    email = data.get("email", "")
    firstName = data.get("firstName", "")
    lastName = data.get("lastName", "")

    if not userName or not password:
        return JsonResponse({"error": "userName and password required"}, status=400)

    # Aynı username varsa
    if User.objects.filter(username=userName).exists():
        return JsonResponse({"error": "Already Registered"}, status=200)

    # Kullanıcı oluştur
    user = User.objects.create_user(username=userName, password=password, email=email)
    user.first_name = firstName
    user.last_name = lastName
    user.save()

    # Oluşturur oluşturmaz login et
    login(request, user)

    return JsonResponse({"userName": userName, "status": True}, status=200)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
