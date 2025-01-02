import requests
import os
from dotenv import load_dotenv
from typing import Dict, List, Union, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
backend_url = os.getenv('BACKEND_URL', 'http://localhost:3030')
sentiment_analyzer_url = os.getenv('SENTIMENT_ANALYZER_URL', 'http://localhost:5050/')
cloudant_url = os.getenv('CLOUDANT_URL', 'https://your-cloudant-url')
api_key = os.getenv('API_KEY')

def get_request(endpoint: str, **kwargs) -> Union[List, Dict]:
    """
    Make a GET request to the backend API with error handling and logging.
    
    Args:
        endpoint (str): The API endpoint to call
        **kwargs: Optional query parameters
    
    Returns:
        Union[List, Dict]: JSON response from the API
    """
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}{'?' + params if params else ''}"
    logger.info(f"Making GET request to: {request_url}")
    
    try:
        response = requests.get(
            request_url,
            headers={'Authorization': f'Bearer {api_key}'} if api_key else None,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error(f"Request timed out for {request_url}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Network exception occurred: {str(e)}")
        return []

def analyze_review_sentiments(text: str) -> Dict:
    """
    Analyze sentiment of review text using sentiment analyzer service.
    
    Args:
        text (str): The review text to analyze
    
    Returns:
        Dict: Sentiment analysis results with fallback to neutral
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    logger.info(f"Analyzing sentiment for text: {text[:50]}...")
    
    try:
        response = requests.get(request_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return {"sentiment": "neutral", "confidence": 0.0}

def post_review(data_dict: Dict) -> Optional[Dict]:
    """
    Post a new review to the backend API with validation.
    
    Args:
        data_dict (Dict): Review data including dealership_id, review_text, etc.
    
    Returns:
        Optional[Dict]: Response from the API or None if failed
    """
    required_fields = ['dealership_id', 'review_text', 'reviewer_name']
    if not all(field in data_dict for field in required_fields):
        logger.error("Missing required fields in review data")
        return None

    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(
            request_url,
            json=data_dict,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else None
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting review: {str(e)}")
        return None

def get_dealers_from_cf(state: Optional[str] = None) -> List[Dict]:
    """
    Fetch dealers from CloudFoundry with optional state filtering.
    
    Args:
        state (Optional[str]): Filter dealers by state if provided
    
    Returns:
        List[Dict]: List of dealer objects with normalized data
    """
    url = f"{cloudant_url}/dealerships"
    if state:
        url += f"?state={state}"
    
    try:
        response = requests.get(
            url,
            headers={'Authorization': f'Bearer {api_key}'} if api_key else None,
            timeout=10
        )
        response.raise_for_status()
        
        dealers_data = response.json()
        dealers = []
        
        for dealer in dealers_data:
            dealer_obj = {
                'id': dealer.get('id'),
                'name': dealer.get('name', 'Unknown Dealer'),
                'address': dealer.get('address', 'No Address'),
                'city': dealer.get('city', 'Unknown City'),
                'state': dealer.get('state', 'Unknown State'),
                'zip': dealer.get('zip', '00000'),
                'phone': dealer.get('phone', 'No Phone'),
                'website': dealer.get('website', ''),
                'rating': dealer.get('rating', 0.0),
                'location': {
                    'lat': dealer.get('lat', 0.0),
                    'lng': dealer.get('lng', 0.0)
                }
            }
            dealers.append(dealer_obj)
        
        return dealers
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching dealers: {str(e)}")
        return []

def get_dealer_reviews(dealer_id: int) -> List[Dict]:
    """
    Fetch reviews for a specific dealer.
    
    Args:
        dealer_id (int): The ID of the dealer
    
    Returns:
        List[Dict]: List of review objects for the dealer
    """
    return get_request(f"/reviews/dealer/{dealer_id}")

def get_dealer_details(dealer_id: int) -> Optional[Dict]:
    """
    Fetch detailed information for a specific dealer.
    
    Args:
        dealer_id (int): The ID of the dealer
    
    Returns:
        Optional[Dict]: Detailed dealer information or None if not found
    """
    try:
        response = get_request(f"/dealers/{dealer_id}")
        return response if response else None
    except Exception as e:
        logger.error(f"Error fetching dealer details: {str(e)}")
        return None