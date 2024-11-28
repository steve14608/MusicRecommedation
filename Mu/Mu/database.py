# -*- coding: utf-8 -*-
from django.http import HttpResponse
from Mus import models


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
        return models.History.filter(user_id=val['user_id'])
    # 返回模型训练后与该歌曲有关的歌
    elif request_name == 'associated_song':
        return models.TrainModel.objects.filter(song_id=val['song_id'])
    # 根据song_id获取歌曲的详细信息
    elif request_name == 'song_info':
        return models.SongInfo.objects.filter(song_id=val['song_id'])
    # 返回头图
    elif request_name == 'avatar':
        return models.Avatar.objects.get(avatar_index=val['avatar_index']).avatar
    elif request_name == 'song_name':
        val = val['song_name']
        return models.SongInfo.objects.raw(f'select distinct songid from rawdata where songname like"{val}"; ')
    elif request_name == 'user_id':
        return models.User.objects.filter(user_id=val['user_id'])



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
        avatar = models.Avatar(user_id=val['user_id'])
        avatar.save()
