from django.db import models
from django.contrib.auth.models import User


class UserDetails(models.Model):
    username = models.CharField(max_length=40, default="", unique=True)


class Followers(models.Model):
    username = models.CharField(max_length=40, default="")
    follow = models.CharField(max_length=40, default="")

    class Meta:
        unique_together = (("username", "follow"))


class Tweets(models.Model):
    username = models.CharField(max_length=40, default="")
    tweet = models.CharField(max_length=150, default="")
    type = models.CharField(max_length=2, default="nt")
    thread = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)


class Likes(models.Model):
    username = models.CharField(max_length=40, default="")
    tweet_id = models.IntegerField(default=0)

    class Meta:
        unique_together = (("username", "tweet_id"))

