# models.py
from django.contrib.auth.models import User
from django.db import models

class UserStripe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_bank_account_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
