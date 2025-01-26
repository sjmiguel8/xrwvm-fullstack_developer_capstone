from django.urls import path

from . import views

app_name = 'djangoapp'
urlpatterns = [
<<<<<<< HEAD
    # Authentication routes - handle the actual authentication logic
    path('', TemplateView.as_view(template_name='Home.html')),
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
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='dealer_by_id'),
    path('fetchDealers/<str:state>', views.get_dealers_by_state, name='dealers_by_state'),

    path('about/', TemplateView.as_view(template_name='About.html')),
    path('contact/', TemplateView.as_view(template_name='index.html')),
    path('get_cars', views.get_cars, name='get_cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    # API endpoints
    path('get_dealers/', views.get_dealers, name='get_dealers'),
    path('dealer/<int:dealer_id>', views.get_dealer_by_id, name='get_dealer'),
    path('fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='get_reviews'),
    path('add_review', views.add_review, name='add_review'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    path('get_car_makes', views.get_car_makes_and_models, name='get_car_makes'),
]
>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
