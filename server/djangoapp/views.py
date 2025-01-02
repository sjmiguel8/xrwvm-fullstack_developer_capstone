from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Review, Dealer
from .restapis import get_request, analyze_review_sentiments, post_review, get_dealers_from_cf
import logging
import json
import requests
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@require_http_methods(["GET", "POST"])
@csrf_exempt
def logout_request(request):
    print("Logout view called")
    logout(request)
    return JsonResponse({
        "status": "success",
        "message": "Successfully logged out"
    }, status=200)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    email = data['email']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')

    try:
        User.objects.get(username=username)
        return JsonResponse({
            "message": "User already exists",
            "userName": username,
            "error": "Already Registered"
        })
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({
            "message": "success",
            "userName": username,
            "status": "Authenticated"
        })

@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        
        if reviews is None:
            return JsonResponse({"status": 404, "message": "No reviews found"})
            
        try:
            for review in reviews:
                sentiment = analyze_review_sentiments(review['review'])
                review['sentiment'] = sentiment.get('sentiment', 'neutral')
            return JsonResponse({"status": 200, "reviews": reviews})
        except Exception as e:
            print(f"Error processing reviews: {str(e)}")
            return JsonResponse({"status": 500, "message": "Error processing reviews"})
            
    return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def get_dealers(request):
    dealers = Dealer.objects.all()
    return render(request, 'djangoapp/dealers.html', {'dealers': dealers})

@csrf_exempt
def get_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state=state)
    dealers_list = list(dealers.values())
    return JsonResponse(dealers_list, safe=False)

@csrf_exempt
def get_dealer_by_id(request, dealer_id):
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

@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            return JsonResponse({"status": 401, "message": f"Error in posting review: {str(e)}"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})

@csrf_exempt
def get_reviews(request):
    reviews = Review.objects.all()
    reviews_list = list(reviews.values())
    return JsonResponse(reviews_list, safe=False)
