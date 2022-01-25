from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    channel_name = models.CharField(max_length=50,unique=True)
    followers = models.IntegerField(default=0)
    streamer = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    follows = models.CharField(max_length=10000,blank=True)