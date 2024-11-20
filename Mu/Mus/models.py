from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class TrainModel(models.Model):
    song_id = models.IntegerField()
    r0 = models.IntegerField()
    r1 = models.IntegerField()
    r2 = models.IntegerField()
    r3 = models.IntegerField()
    r4 = models.IntegerField()
    r5 = models.IntegerField()
    r6 = models.IntegerField()
    r7 = models.IntegerField()
    r8 = models.IntegerField()
    r9 = models.IntegerField()


class SongInfo(models.Model):
    song_id = models.IntegerField()
    song_name = models.CharField(max_length=32)
    song_singer = models.CharField(max_length=18)


class User(models.Model):
    user_id = models.IntegerField()
    user_account = models.IntegerField()
    user_password = models.CharField(max_length=18)
    user_avatar = models.IntegerField()
    user_bio = models.CharField(32)
    user_nickname = models.CharField(16)


class History(models.Model):
    user_id = models.IntegerField()
    song_id = models.IntegerField()
    last_time = models.TimeField()


class Avatar(models.Model):
    avatar_index = models.IntegerField()
    avatar = models.ImageField()
