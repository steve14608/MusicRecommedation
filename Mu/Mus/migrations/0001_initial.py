# Generated by Django 5.1.3 on 2024-12-01 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('avatar', models.ImageField(upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('song_id', models.IntegerField()),
                ('last_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SongInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.IntegerField()),
                ('song_name', models.CharField(max_length=32)),
                ('song_singer', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('user_account', models.IntegerField()),
                ('user_password', models.CharField(max_length=18)),
                ('user_avatar', models.IntegerField()),
                ('user_bio', models.CharField(default='无', max_length=32)),
                ('user_nickname', models.CharField(default='默认用户', max_length=16)),
            ],
        ),
    ]
