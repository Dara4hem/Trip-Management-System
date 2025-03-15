from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Trip

class TripAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.trip = Trip.objects.create(
            current_location="Cairo",
            pickup_location="Alexandria",
            dropoff_location="Giza",
            current_latitude=30.0444,
            current_longitude=31.2357,
            dropoff_latitude=30.0131,
            dropoff_longitude=31.2089
        )

    def test_trip_route_api(self):
        url = reverse('trip-route', args=[self.trip.id])  
        response = self.client.get(url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertIn('route_summary', response.json())  
        self.assertIn('estimated_time_hours', response.json()) 
        self.assertIn('estimated_distance_km', response.json()) 

