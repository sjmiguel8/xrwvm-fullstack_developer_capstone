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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from djangoapp.views import (AboutView, ContactView, DealerDetailView,
                             DealersView, HomeView, LoginView, PostReviewView,
                             RegisterView)

urlpatterns = [
<<<<<<< HEAD
    # Static pages using TemplateView
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    path('index/', TemplateView.as_view(template_name="index.html"), name='index'),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="index.html")),
    
    # React routes - all serve index.html
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:id>/', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),
=======
    # Template views
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dealers/', DealersView.as_view(), name='dealers'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dealer/<int:id>/', DealerDetailView.as_view(), name='dealer_details'),
    path('postreview/<int:dealer_id>/', PostReviewView.as_view(), name='post_review'),
>>>>>>> 5640e36cdccbbac143706c3b2726d6031e25c264
    
    # API endpoints
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
