from django.db import models

class Game(models.Model):
    match = models.CharField(max_length=255)
    time = models.DateTimeField()
    pick = models.CharField(max_length=255)
    odd = models.DecimalField(max_digits=5, decimal_places=2)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.match
