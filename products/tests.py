from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Product

class ProductTests(APITestCase):

    def test_create_product(self):
        url = reverse('product-list')
        data = {'name': 'Test Product', 'description': 'Test Description', 'price': 9.99}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
