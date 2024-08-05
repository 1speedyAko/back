from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription

User = get_user_model()

class SubscriptionModelTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(email='test@user.com', password='12345')
        self.silver_plan = SubscriptionPlan.objects.create(
            name='Silver Plan',
            description='1 month silver plan',
            price=49.9,
            category='silver'
        )
        self.gold_plan = SubscriptionPlan.objects.create(
            name='Gold Plan',
            description='2 months gold plan',
            price=89.9,
            category='gold'
        )
        self.platinum_plan = SubscriptionPlan.objects.create(
            name='Platinum Plan',
            description='3 months platinum plan',
            price=129.9,
            category='platinum'
        )

    def test_create_subscription_plan(self):
        """ Test creating a subscription plan """
        plan = SubscriptionPlan.objects.create(
            name='Test Plan',
            description='Test description',
            price=100.0,
            category='silver'
        )
        self.assertEqual(plan.name, 'Test Plan')
        self.assertEqual(plan.price, 100.0)
        self.assertEqual(plan.category, 'silver')

    def test_user_subscription_creation(self):
        """ Test creating a user subscription """
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.silver_plan,
            start_date=timezone.now()
        )
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.silver_plan)
        self.assertTrue(subscription.end_date)

    def test_subscription_end_date_calculation(self):
        """ Test end date is set correctly based on plan category """
        now = timezone.now()

        # Test Silver Plan
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.silver_plan,
            start_date=now
        )
        expected_end_date = now + timedelta(days=30)
        self.assertEqual(subscription.end_date.date(), expected_end_date.date())

        # Test Gold Plan
        subscription.plan = self.gold_plan
        subscription.end_date = None  # Reset end_date to force recalculation
        subscription.save()
        expected_end_date = now + timedelta(days=60)
        self.assertEqual(subscription.end_date.date(), expected_end_date.date())

        # Test Platinum Plan
        subscription.plan = self.platinum_plan
        subscription.end_date = None  # Reset end_date to force recalculation
        subscription.save()
        expected_end_date = now + timedelta(days=90)
        self.assertEqual(subscription.end_date.date(), expected_end_date.date())


    def test_subscription_status_active(self):
        """ Test subscription status is active when valid """
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.silver_plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.assertTrue(subscription.is_active())

    def test_subscription_status_expired(self):
        """ Test subscription status is expired when not valid """
        subscription = UserSubscription.objects.create(
            user=self.user,
            plan=self.silver_plan,
            start_date=timezone.now() - timedelta(days=40),
            end_date=timezone.now() - timedelta(days=10)
        )
        self.assertFalse(subscription.is_active())
