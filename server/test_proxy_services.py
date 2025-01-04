import requests


def test_proxy_services():
    base_url = "http://127.0.0.1:8000/djangoapp"
    
    print("\n1. Testing Dealer Reviews:")
    response = requests.get(f"{base_url}/fetchReviews/dealer/29")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n2. Testing All Dealers:")
    response = requests.get(f"{base_url}/fetchDealers")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n3. Testing Dealer by ID:")
    response = requests.get(f"{base_url}/fetchDealer/3")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n4. Testing Dealers by State:")
    response = requests.get(f"{base_url}/fetchDealers/Kansas")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_proxy_services() 