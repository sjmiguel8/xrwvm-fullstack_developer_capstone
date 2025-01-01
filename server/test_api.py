import requests

def test_reviews_endpoint():
    # Test getting all reviews
    response = requests.get('http://127.0.0.1:8000/djangoapp/reviews/')
    
    # Print response status and data
    print(f"Status Code: {response.status_code}")
    print("Response Data:", response.json())
    
    # Basic assertions
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Verify it returns a list

if __name__ == "__main__":
    test_reviews_endpoint() 