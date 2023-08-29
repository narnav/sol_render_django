from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Trips(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=50)
    createdTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.description:
            return self.description
        return "Unnamed Trip"


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    desc = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    currency = models.CharField(max_length=4)
    createdTime = models.DateTimeField(default=timezone.now)
    trip = models.ForeignKey(Trips, related_name='expenses', on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if self.trip.user != self.user:
            raise ValueError('Only trip creator can add expenses!')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.desc} - {self.price} {self.currency}"
    


class CurrencyRate(models.Model):
    base_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    exchange_rate = models.FloatField()
    time_utc = models.DateTimeField()

    def __str__(self):
        return f"{self.base_currency}/{self.target_currency} - {self.exchange_rate}"
