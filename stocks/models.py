from django.db import models
from django.contrib.auth.models import User

class Trade_idea(models.Model):
    user = models.CharField(max_length=30)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    open_price = models.DecimalField(max_digits=8, decimal_places=2)
    close_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    current_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    performance = models.CharField(max_length=10, blank=True, null=True)
    target_price = models.DecimalField(max_digits=8, decimal_places=2)
    upside = models.CharField(max_length=10, blank=True, null=True)
    message = models.CharField(max_length=300)
    open_date = models.CharField(max_length=10)
    close_date = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} / {self.ticker} / {self.status}"




# Create your models here.
