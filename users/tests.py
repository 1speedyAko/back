from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
