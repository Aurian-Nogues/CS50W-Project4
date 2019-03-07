from django.db import models
from django.contrib.auth.models import User

class Trade_idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    open_price = models.DecimalField(max_digits=8, decimal_places=2)
    close_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    message = models.CharField(max_length=300)
    open_date = models.CharField(max_length=10)
    close_date = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} / {self.ticker} / {self.status}"




# Create your models here.
