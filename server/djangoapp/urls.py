from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # API endpoints
    path('get_dealers/', views.get_dealers, name='get_dealers'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
]
