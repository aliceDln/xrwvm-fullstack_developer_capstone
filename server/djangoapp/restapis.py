# Imports
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

# Backend URLs
backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)

# -------------------------
# GET request to backend
# -------------------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + value + "&"

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except Exception as err:
        print("Network exception occurred")
        print(err)
        return None


# ------------------------------------
# Analyze review sentiment (microservice)
# ------------------------------------
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + quote(text)
    try:
        response = requests.get(request_url, timeout=10)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"label": "neutral"}


# -------------------------
# POST review to backend
# -------------------------
def post_review(data_dict):
    request_url = backend_url + "/reviews"
    try:
        response = requests.post(
            request_url,
            json=data_dict,
            timeout=10
        )
        return response.json()
    except Exception as err:
        print("Error posting review")
        print(err)
        return None
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=10)
        print(response.json())
        return response.json()
    except Exception as err:
        print("Network exception occurred")
        print(err)
        return None
