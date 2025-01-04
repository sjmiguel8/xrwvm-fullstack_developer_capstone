import requests


def test_dealers():
    print("\nTesting Dealers API:")
    response = requests.get('http://localhost:8000/djangoapp/fetchDealers')
    print(f"Status Code: {response.status_code}")
    print("Response Data:", response.json())

if __name__ == "__main__":
    test_dealers() 