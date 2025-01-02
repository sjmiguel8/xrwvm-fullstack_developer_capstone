# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.generic import TemplateView


app_name = 'djangoapp'
urlpatterns = [
    # Authentication routes - handle the actual authentication logic
    path('register', views.registration, name='register_submit'),
    path('login', views.login_user, name='login_submit'),
    path('logout/', views.logout_request, name='logout'),

    # Review routes
    path('reviews/', views.get_reviews, name='reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),

    # Dealer routes
    path('get_dealers/', views.get_dealers, name='get_dealers'),
    path('fetchDealers', views.get_dealers, name='all_dealers'),
    path('fetchDealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('fetchDealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
