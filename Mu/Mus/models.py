from django.db import models

# Create your models here.
from django.db import models


# Create your models here.python3 manage.py migrate

class SongInfo(models.Model):
    song_id = models.IntegerField()
    song_name = models.CharField(max_length=64)
    song_singer = models.CharField(max_length=32)
    song_singer_id = models.IntegerField()


class User(models.Model):
    user_id = models.IntegerField()
    user_account = models.IntegerField()
    user_password = models.CharField(max_length=18)
    user_avatar = models.IntegerField()
    user_bio = models.CharField(max_length=32, default='无')
    user_nickname = models.CharField(max_length=16, default='默认用户')


class History(models.Model):
    user_id = models.IntegerField()
    song_id = models.IntegerField()
    last_time = models.IntegerField()


class Avatar(models.Model):
    user_id = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars/')
