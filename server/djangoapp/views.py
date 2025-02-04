import json
import logging

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import CarMake, CarModel, Dealer, Review
from .restapis import (analyze_review_sentiments, get_dealers_from_cf,
                       get_request, post_review)


# Template views
class HomeView(TemplateView):
    """View for the home page."""
    template_name = "Home.html"

class AboutView(TemplateView):
    template_name = "About.html"

class ContactView(TemplateView):
    template_name = "Contact.html"

class DealersView(TemplateView):
    template_name = "dealers.html"

class LoginView(TemplateView):
    template_name = "login.html"

class RegisterView(TemplateView):
    template_name = "register.html"

class DealerDetailView(TemplateView):
    template_name = "dealer_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer_id = self.kwargs.get('id')
        try:
            dealer = Dealer.objects.get(id=dealer_id)
            context['dealer'] = dealer
            context['reviews'] = Review.objects.filter(dealership=dealer_id)
        except Dealer.DoesNotExist:
            context['error'] = 'Dealer not found'
        return context

class PostReviewView(TemplateView):
    template_name = "post_review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dealer_id = self.kwargs.get('dealer_id')
        try:
            dealer = Dealer.objects.get(id=dealer_id)
            context['dealer'] = dealer
        except Dealer.DoesNotExist:
            context['error'] = 'Dealer not found'
        return context

# API views
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

@csrf_exempt
def get_dealers(request):
    try:
        dealers = Dealer.objects.all()
        dealers_list = []
        for dealer in dealers:
            dealers_list.append({
                "id": dealer.id,
                "full_name": dealer.full_name,
                "city": dealer.city,
                "address": dealer.address,
                "state": dealer.state,
                "zip": dealer.zip,
                "short_name": dealer.short_name
            })
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        print(f"Error in get_dealers: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

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
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({
            'message': 'Registration successful',
            'username': user.username
        })
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

@csrf_exempt
def logout_request(request):
    try:
        logout(request)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def get_reviews(request):
    reviews = Review.objects.all()
    reviews_list = list(reviews.values())
    return JsonResponse(reviews_list, safe=False)

@csrf_exempt
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = Review.objects.filter(dealership=dealer_id)
        reviews_list = [{
            'name': review.name,
            'dealership': review.dealership,
            'review': review.review,
            'purchase': review.purchase,
            'purchase_date': review.purchase_date,
            'car_make': review.car_make,
            'car_model': review.car_model,
            'car_year': review.car_year,
        } for review in reviews]
        return JsonResponse({"status": 200, "reviews": reviews_list})
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})

@csrf_exempt
def add_review(request):
    try:
        data = json.loads(request.body)
        review = Review.objects.create(
            name=data['name'],
            dealership=data['dealership'],
            review=data['review'],
            purchase=data.get('purchase', True),
            purchase_date=data['purchase_date'],
            car_make=data.get('car_make', ''),
            car_model=data.get('car_model', ''),
            car_year=data.get('car_year', '')
        )
        return JsonResponse({
            "status": 200,
            "review": {
                "name": review.name,
                "dealership": review.dealership,
                "review": review.review,
                "purchase": review.purchase,
                "purchase_date": review.purchase_date,
                "car_make": review.car_make,
                "car_model": review.car_model,
                "car_year": review.car_year
            }
        })
    except Exception as e:
        return JsonResponse({"status": 500, "message": str(e)})

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
                "full_name": dealer.full_name,
                "short_name": dealer.short_name
            }]
        })
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"})

@csrf_exempt
def get_dealers_by_state(request, state):
    try:
        dealers = Dealer.objects.filter(state=state)
        dealers_list = list(dealers.values())
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_cars(request):
    car_models = [
        {"CarMake": "Honda", "CarModel": "Civic"},
        {"CarMake": "Honda", "CarModel": "Accord"},
        {"CarMake": "Toyota", "CarModel": "Camry"},
        {"CarMake": "Toyota", "CarModel": "Corolla"},
        {"CarMake": "Ford", "CarModel": "F-150"},
        {"CarMake": "Ford", "CarModel": "Mustang"},
        {"CarMake": "Chevrolet", "CarModel": "Silverado"},
        {"CarMake": "Chevrolet", "CarModel": "Camaro"}
    ]
    return JsonResponse({
        "status": 200,
        "CarModels": car_models
    })

@csrf_exempt
def get_car_makes_and_models(request):
    try:
        makes = CarMake.objects.all()
        makes_data = []
        for make in makes:
            models = make.carmodel_set.all()
            makes_data.append({
                'name': make.name,
                'description': make.description,
                'models': [
                    {
                        'name': model.name,
                        'type': model.car_type,
                        'year': model.year
                    } for model in models
                ]
            })
        return JsonResponse({'makes': makes_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
