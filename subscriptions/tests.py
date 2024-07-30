from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.utils import timezone
from .models import UserSubscription
from payments.models import Payment
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class WebhookTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@user.com', password='12345')
        self.product = Product.objects.create(name='Test Product', description='Test', price=10.00)
        self.payment = Payment.objects.create(
            order_id='123',
            user=self.user,
            product=self.product,
            amount=49,
            currency='USD',
            status='pending',
            transaction_id='tx123'
        )

    def test_webhook_confirmation(self):
        payload = {
            "transaction_id": "tx123",
            "status": "confirmed",
            "period": "1_month"
        }
        signature = "valid_signature"  # Generate or mock a valid signature

        response = self.client.post(
            reverse('cryptomus-webhook'),
            data=payload,
            HTTP_SIGN=signature
        )

        self.assertEqual(response.status_code, 200)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'confirmed')
        subscription = UserSubscription.objects.get(user=self.user)
        self.assertEqual(subscription.status, 'active')
