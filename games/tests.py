from django.test import TestCase
from .models import Game
from django.contrib.auth import get_user_model

user = get_user_model()

class GameTest(TestCase):
    def setUp(self):
       self.gaming = Game.objects.create(match="team_a vs team_b",pick="team_a" ,odd=2.22, is_premium=False)
        

    def test_game_creation(self):
        gaming = Game.objects.get(pick="team_a")
        self.assertEqual(gaming.match, "team_a vs team_b")
        self.assertEqual(gaming.pick, "team_a")
        self.assertEqual(gaming.odd, 2.22)
        # self.assertEqual(gaming.time, )















