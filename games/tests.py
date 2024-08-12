# from django.test import TestCase
# from .models import Game
# from django.contrib.auth import get_user_model

# user = get_user_model()

# class GameTest(TestCase):
#     def setUp(self):
#        self.gaming = Game.objects.create(match="team_a vs team_b",pick="team_a" ,odd=2.22, is_premium=False)
        

#     def test_game_creation(self):
#         gaming = Game.objects.get(pick="team_a")
#         self.assertEqual(gaming.match, "team_a vs team_b")
#         self.assertEqual(gaming.pick, "team_a")
#         self.assertEqual(gaming.odd, 2.22)
#         # self.assertEqual(gaming.time, )


from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Game
from subscriptions.models import SubscriptionPlan, UserSubscription

User = get_user_model()

# class GameModelTest(TestCase):

#     def setUp(self):
#         # This method is called before every test case
#         self.game = Game.objects.create(
#             match="Team A vs Team B",
#             time=timezone.now(),
#             pick="Team A",
#             odd=1.5,
#             is_premium=True
#         )

#     def test_game_creation(self):
#         # Test that the game instance is created correctly
#         self.assertEqual(self.game.match, "Team A vs Team B")
#         self.assertEqual(self.game.pick, "Team A")
#         self.assertEqual(self.game.odd, 1.5)
#         self.assertTrue(self.game.is_premium)
#         self.assertIsInstance(self.game.time, timezone.datetime)

#     def test_game_string_representation(self):
#         # Test the string representation of the Game model
#         expected_string = f"{self.game.match} at {self.game.time} - Pick: {self.game.pick} (Odds: {self.game.odd})"
#         self.assertEqual(str(self.game), expected_string)





class GameViewsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@user.com', password='password')
        self.plan = SubscriptionPlan.objects.create(name='Platinum', category='platinum', price=129.9)
        self.subscription = UserSubscription.objects.create(user=self.user, plan=self.plan, start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=30), status='active')

        self.free_game = Game.objects.create(
            match="Team C vs Team D",
            time=timezone.now(),
            pick="Team C to win",
            odd=2.0,
            is_premium=False
        )

        self.premium_game = Game.objects.create(
            match="Team E vs Team F",
            time=timezone.now(),
            pick="Team E to win",
            odd=1.7,
            is_premium=True
        )

    def test_free_odds_list_view(self):
        """Test that the FreeOddsListView returns only free games"""
        self.client.force_authenticate(user=self.user)
        url = reverse('free-odds')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['is_premium'], False)

    def test_premium_picks_list_view_with_subscription(self):
        """Test that the PremiumPicksListView returns premium games for subscribed users"""
        self.client.force_authenticate(user=self.user)
        url = reverse('premium-picks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['is_premium'], True)

    def test_premium_picks_list_view_without_subscription(self):
        """Test that the PremiumPicksListView returns no games for unsubscribed users"""
        self.subscription.delete()  # Removing the subscription
        self.client.force_authenticate(user=self.user)
        url = reverse('premium-picks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)









