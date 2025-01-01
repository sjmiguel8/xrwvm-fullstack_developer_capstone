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
def get_dealer_by_id(request, id):
    """Fetch dealer by ID"""
    if request.method == 'GET':
        try:
            dealer = Dealer.objects.get(id=id)
            return JsonResponse(dealer.__dict__, safe=False)
        except Dealer.DoesNotExist:
            return JsonResponse({'error': 'Dealer not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
