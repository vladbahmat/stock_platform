from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    customer_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}"