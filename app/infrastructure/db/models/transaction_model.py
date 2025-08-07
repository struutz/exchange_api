from django.db import models


class TransactionModel(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=5)
    category = models.CharField(max_length=20)
    date = models.DateField()
    description = models.TextField()