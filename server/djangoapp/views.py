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
from .populate import initiate
from .models import Review, Dealer  # Make sure to import your Review and Dealer models
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}

    data = json.loads(request.body)
    username = data['username']  # Changed from userName
    password = data['password']
    email = data['email']
    # Set default values for first_name and last_name if not provided
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')

    username_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        # Login the user and redirect to list page
        login(request, user)
        return JsonResponse({
            "message": "success",
            "userName": username,
            "status": "Authenticated"
        })
    else:
        return JsonResponse({
            "message": "User already exists",
            "userName": username,
            "error": "Already Registered"
        })

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `add_review` view to submit a review
# def add_review(request):
# ...

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

@csrf_exempt
def get_reviews(request):
    if request.method == 'GET':
        # Get all reviews from the database
        reviews = Review.objects.all()
        # Convert reviews to list of dictionaries
        reviews_list = list(reviews.values())
        return JsonResponse(reviews_list, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_dealers(request):
    """Fetch all dealers"""
    if request.method == 'GET':
        dealers = Dealer.objects.all()
        dealers_list = list(dealers.values())
        return JsonResponse(dealers_list, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_dealers_by_state(request, state):
    """Fetch dealers by state"""
    if request.method == 'GET':
        dealers = Dealer.objects.filter(state=state)
        dealers_list = list(dealers.values())
        return JsonResponse(dealers_list, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_dealer_by_id(request, dealer_id):
    """Fetch dealer by ID"""
    if request.method == 'GET':
        try:
            dealer = Dealer.objects.get(id=dealer_id)
            return JsonResponse({
                "dealer": {
                    "id": dealer.id,
                    "name": dealer.name,
                    "address": dealer.address,
                    "city": dealer.city,
                    "state": dealer.state,
                    "zip_code": dealer.zip_code
                }
            })
        except Dealer.DoesNotExist:
            return JsonResponse({'error': 'Dealer not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
