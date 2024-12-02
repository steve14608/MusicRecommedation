# -*- coding: utf-8 -*-
from django.http import HttpResponse
from Mus import models
from django.db import connection


# 数据库操作
def testdb(request):
    test = models.SongInfo.objects.get(id=2)
    print(test.song_name)
    return HttpResponse("<p>数据添加成功！</p>")


def query(request_name, val):
    # 用户登录
    if request_name == 'user':
        return models.User.objects.filter(user_account=val['user_account'], user_password=val['user_password'])
    # 用户账号是否唯一
    elif request_name == 'user_account':
        return len(models.User.objects.filter(user_account=val['user_account'])) > 0
    # 听歌历史
    elif request_name == 'user_history':
        # return models.History.objects.raw(f'select songid from history where user_id = {val} order by last_time desc')
        return models.History.objects.filter(user_id=val['user_id']).order_by('-last_time')
    # 根据song_id获取歌曲的详细信息
    elif request_name == 'song_info':
        return models.SongInfo.objects.filter(song_id=val['song_id'])
    elif request_name == 'singer_id':
        # return models.SongInfo.objects.raw(f'select singerid from rawdata5 where songid = {val}')
        cursor = connection.cursor()
        cursor.execute('select singer_id from rawedata5 where song_id = %s', [val['singer_id']])
        return cursor.fetchall()
    # 返回头图
    elif request_name == 'avatar':
        return models.Avatar.objects.get(avatar_index=val['avatar_index']).avatar
    elif request_name == 'song_name':
        # return models.SongInfo.objects.raw(f'select distinct songid from rawdata where songname like"{val}"; ')
        cursor = connection.cursor()
        cursor.execute('select distinct song_id,song_name,song_singer,song_singer_id from mus_songinfo where songname '
                       'like %s ', [val['song_name']])
        return cursor.fetchall()
    elif request_name == 'user_id':
        return models.User.objects.filter(user_id=val['user_id'])
    elif request_name=='song_singer_id':
        return models.SongInfo.objects.filter(song_singer_id=val['song_singer_id'])


def update(request_name, val):
    if request_name == 'user':
        user = models.User.objects.get(user_id=val['user_id'])
        if val.get('user_avatar') is not None:
            user.user_avatar = val['user_avatar']
        if val.get('user_bio') is not None:
            user.user_bio = val['user_bio']
        if val.get('user_nickname') is not None:
            user.user_nickname = val['user_nickname']
        user.save()
    elif request_name == 'history':
        history = models.History.objects.get(user_id=val['user_id'], song_id=val['song_id'])
        history.last_time = val['last_time']
        history.save()
    elif request_name == 'avatar':
        avatar = models.Avatar.objects.get(avatar_index=val)
        avatar.avatar = val['avatar']
        avatar.save()


def insert(request_name, val):
    if request_name == 'user':
        user = models.User(user_id=val['user_id'], user_account=val['user_account'], user_password=val['user_password']
                           , user_avatar=val['user_avatar'], user_bio=val['user_bio']
                           , user_nickname=val['user_nickname'])
        user.save()
    elif request_name == 'history':
        history = models.History(user_id=val['user_id'], song_id=val['song_id'], last_time=val['last_time'])
        history.save()
    elif request_name == 'avatar':
        avatar = models.Avatar(avatar_index=val['user_id'])
        avatar.save()
