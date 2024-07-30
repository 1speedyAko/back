from django.test import TestCase
from django.contrib.auth import get_user_model
from payments.models import Payment
from products.models import Product

User = get_user_model()

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='tes@tuser.com', password='12345')
        self.product = Product.objects.create(name='Test Product', description='Test', price=10.00)
        self.payment = Payment.objects.create(
            order_id='123',
            user=self.user,
            product=self.product,
            amount=10.00,
            currency='USD',
            status='pending',
            transaction_id='tx123'
        )

    def test_payment_creation(self):
        payment = Payment.objects.get(order_id='123')
        self.assertEqual(payment.user.email, 'tes@tuser.com')
        self.assertEqual(payment.product.name, 'Test Product')
        self.assertEqual(payment.amount, 10.00)
        self.assertEqual(payment.status, 'pending')
