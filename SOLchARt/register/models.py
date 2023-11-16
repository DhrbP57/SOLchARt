# register/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Dodaj dodatkowe pola profilu, jeśli są potrzebne
    # np. avatar, data urodzenia, itp.

    def __str__(self):
        return self.user.username