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
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        return JsonResponse({
            'message': 'Registration successful',
            'username': user.username
        })
        
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

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
    try:
        dealers = Dealer.objects.all()
        dealers_list = []
        for dealer in dealers:
            dealers_list.append({
                'id': dealer.id,
                'name': dealer.full_name,
                'city': dealer.city,
                'state': dealer.state,
                'address': dealer.address,
                'zip': dealer.zip,
                'lat': dealer.lat,
                'long': dealer.long,
                'short_name': dealer.short_name,
                'st': dealer.st
            })
        print("Sending dealers:", dealers_list)
        response = JsonResponse(dealers_list, safe=False)
        response['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print(f"Error in get_dealers: {str(e)}")
        return JsonResponse(
            {'error': str(e)}, 
            status=500, 
            content_type='application/json'
        )

@csrf_exempt
def get_dealers_by_state(request, state):
    try:
        dealers = Dealer.objects.filter(state=state)
        dealers_list = list(dealers.values())
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
        return JsonResponse({
            "status": 200,
            "dealer": [{
                "id": dealer.id,
                "name": dealer.full_name,
                "city": dealer.city,
                "address": dealer.address,
                "zip": dealer.zip,
                "state": dealer.state,
                "st": dealer.st,
                "full_name": dealer.full_name
            }]
        })
    except Dealer.DoesNotExist:
        return JsonResponse({
            "status": 404,
            "message": "Dealer not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "status": 500,
            "message": str(e)
        }, status=500)

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
