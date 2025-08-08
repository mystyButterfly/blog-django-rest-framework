from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here. start unit-test branch

class ViewRootTest(APITestCase):
    def test_root_view(self):
        response = self.client.get(reverse('root-api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Welcome to the Django REST Framework API!')
