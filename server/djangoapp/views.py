# Uncomment the required imports before adding the code
from .models import CarMake, CarModel
from .populate import initiate

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt

import logging
import json
from datetime import datetime

from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -----------------------------
# AUTH: LOGIN / LOGOUT / REGISTER
# -----------------------------
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


# -----------------------------
# CARS (CarMake / CarModel) JSON
# -----------------------------
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# -----------------------------
# DEALERSHIPS (Proxy to backend)
# -----------------------------
# Update the `get_dealerships` render list of dealerships all by default,
# particular state if state is passed
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Get one dealer's details by dealer_id
def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealer = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealer})


# Get dealer reviews + enrich each review with sentiment from microservice
def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    if not reviews:
        return JsonResponse({"status": 200, "reviews": []})

    for review_detail in reviews:
        try:
            text = review_detail.get("review", "")
            sentiment_res = analyze_review_sentiments(text) or {}
            review_detail["sentiment"] = sentiment_res.get("label", "neutral")
        except Exception:
            review_detail["sentiment"] = "neutral"

    return JsonResponse({"status": 200, "reviews": reviews})
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous is False:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200, "message": "Review posted"})
        except Exception:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
