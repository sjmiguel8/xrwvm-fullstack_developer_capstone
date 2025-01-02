import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Make a GET request to the backend API
    """
    params = ""
    if kwargs:
        params = "&".join(f"{key}={value}" for key, value in kwargs.items())

    request_url = f"{backend_url}{endpoint}{'?' + params if params else ''}"
    print(f"GET from {request_url}")
    
    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {str(e)}")
        return []  # Return empty list instead of None

def analyze_review_sentiments(text):
    """
    Analyze sentiment of review text using sentiment analyzer service
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Sentiment analysis error: {str(e)}")
        return {"sentiment": "neutral"}  # Default fallback

def post_review(data_dict):
    """
    Post a new review to the backend API
    """
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        print(f"Error posting review: {str(e)}")
        return None