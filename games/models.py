# games/models.py

from django.db import models

class Game(models.Model):
    match = models.CharField(max_length=255)
    time = models.DateTimeField()
    pick = models.CharField(max_length=255)  
    odd = models.FloatField()
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.match} at {self.time} - Pick: {self.pick} (Odds: {self.odd})"

