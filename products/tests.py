from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', description='Test', price=10.00)

    def test_product_creation(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test')
        self.assertEqual(product.price, 10.00)

# Add more tests to cover different aspects of the product functionality
