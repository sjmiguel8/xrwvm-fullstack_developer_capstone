from django.test import Client, TestCase
from django.urls import reverse

from .models import Review  # Import your Review model


class ReviewAPITest(TestCase):
    def setUp(self):
        # Create test data
        self.client = Client()
        # Add some test reviews if needed
        
    def test_get_reviews(self):
        # Test the reviews endpoint
        response = self.client.get(reverse('djangoapp:reviews'))
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
        # Print response data for inspection
        print("Test Response:", response.json()) 