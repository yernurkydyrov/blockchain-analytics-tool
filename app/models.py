from django.db import models


class AccountBalances(models.Model):
    adress = models.CharField(max_length=30)
    balance = models.PositiveIntegerField()
