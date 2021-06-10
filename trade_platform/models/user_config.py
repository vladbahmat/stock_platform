from django.contrib.auth.models import User
from django.db import models


class UserConfig(models.Model):
    LANGUAGE_CODE = [
        ('en', 'English'),
        ('ru', 'Russian'),
        ('ch', 'Chinese'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="config")
    language_code = models.CharField(max_length=2, choices=LANGUAGE_CODE, default='en')