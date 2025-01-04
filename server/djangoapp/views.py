"""djangoproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views as djangoapp_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from djangoapp.views import HomeView, AboutView, ContactView, DealersView, LoginView, RegisterView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from .models import Review, Dealer
from .restapis import get_request, analyze_review_sentiments, post_review, get_dealers_from_cf
import logging
import json
import requests

urlpatterns = [
    # Use the class-based views
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dealers/', DealersView.as_view(), name='dealers'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Keep these the same
    path('dealer/<int:id>/', TemplateView.as_view(template_name="Home.html")),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="Home.html")),
    
    # API endpoints
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Define template views first
class HomeView(TemplateView):
    template_name = "Home.html"

class AboutView(TemplateView):
    template_name = "Home.html"

class ContactView(TemplateView):
    template_name = "Home.html"

class DealersView(TemplateView):
    template_name = "Home.html"

class LoginView(TemplateView):
    template_name = "Home.html"

class RegisterView(TemplateView):
    template_name = "Home.html"

# API Views
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
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        return HttpResponseServerError(f"Server error: {str(e)}")

# Add all your other view functions here...
