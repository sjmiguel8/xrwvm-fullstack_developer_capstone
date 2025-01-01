# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('register', views.registration, name='register'),

    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for dealer reviews view

    # path for add a review view
    path('logout', views.logout_request, name='logout'),

    # Add this new path for reviews
    path('reviews/', views.get_reviews, name='reviews'),

    # New dealer endpoints
    path('dealers/', views.get_dealers, name='get_dealers'),
    path('dealers/<str:state>/', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path('fetchDealers', views.get_dealers, name='get_dealers'),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('fetchDealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
