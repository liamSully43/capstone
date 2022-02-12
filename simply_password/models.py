from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.username

class WebPassword(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    # attach the password to the user by saving the user's id within the password model
    user_id = models.IntegerField()

    def __str__(self):
            return self.url