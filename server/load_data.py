import os
import django
import json
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')
django.setup()

from djangoapp.models import Dealer, Review

def load_dealers():
    # Get the path to dealerships.json
    json_path = Path(__file__).parent / 'database' / 'data' / 'dealerships.json'
    
    with open(json_path) as f:
        dealers_data = json.load(f)
        
    for dealer in dealers_data['dealerships']:
        Dealer.objects.get_or_create(
            id=dealer['id'],
            city=dealer['city'],
            state=dealer['state'],
            st=dealer['st'],
            address=dealer['address'],
            zip=dealer['zip'],
            lat=str(dealer['lat']),
            long=str(dealer['long']),
            short_name=dealer['short_name'],
            full_name=dealer['full_name']
        )
    print(f"Loaded {len(dealers_data['dealerships'])} dealers")

def load_reviews():
    # Get the path to reviews.json
    json_path = Path(__file__).parent / 'database' / 'data' / 'reviews.json'
    
    with open(json_path) as f:
        reviews_data = json.load(f)
        
    for review in reviews_data['reviews']:
        Review.objects.get_or_create(
            name=review['name'],
            dealership=review['dealership'],
            review=review['review'],
            purchase=review['purchase'],
            purchase_date=review['purchase_date'],
            car_make=review['car_make'],
            car_model=review['car_model'],
            car_year=review['car_year']
        )
    print(f"Loaded {len(reviews_data['reviews'])} reviews")

if __name__ == '__main__':
    load_dealers()
    load_reviews() 