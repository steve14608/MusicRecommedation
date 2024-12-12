import json
from collections import defaultdict

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import database
import time
import os
from . import song
from Mus.model_manager import model_manager


# 初始界面.判断有没有cookie来确定是去登录界面还是主页面
def page(request):
    if request.COOKIES.get('user_id') is None:
        return render(request, 'login1.html')
    else:
        temp = database.query(request_name='user_id', val={'user_id': request.COOKIES.get('user_id')})
        if len(temp) == 0:
            # request.delete_cookie('user_id')
            temp = render(request, 'login1.html')
            temp.delete_cookie('user_id')
            return temp
        return render(request, 'main.html')


# 登录
def login(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)

    val = {"user_account": json_data['user_account'], "user_password": json_data['user_password']}
    user = database.query(request_name='user', val=val)

    if len(user) > 0:
        user = user.first()
        user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                     "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
        rep = HttpResponse(json.dumps(user_info), status=200)
        rep.set_cookie('user_id', user.user_id)
        return rep
    else:
        return HttpResponse(status=404)
    pass


# 注册
def signup(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {"user_account": json_data['user_account'], "user_password": json_data['user_password']}
    if database.query(request_name='user_account', val=val):
        return HttpResponse(status=404)
    else:
        ti = int(time.time())
        user = {'user_account': val['user_account'], 'user_password': val['user_password'], 'user_id': ti,
                'user_avatar': ti, 'user_bio': '无', 'user_nickname': '默认'}
        database.insert(request_name='user', val=user)
        avatar = {'avatar_index': ti}
        database.insert(request_name='avatar', val=avatar)
        rep = HttpResponse(content=ti, status=200)
        rep.set_cookie('user_id', ti)
        return rep


# 更新头图
def updateAvatar(request):
    val = {'user_id': request.COOKIES.get('user_id'), 'avatar': request.FILES.get('avatar')}

    database.update(request_name='avatar', val=val)
    return HttpResponse(status=200)


# 更新签名和昵称
def updateInfo(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {'user_id': request.COOKIES.get('user_id'), 'user_nickname': json_data['user_nickname'],
           'user_bio': json_data['user_bio']}

    database.update('user', val)
    return HttpResponse(status=200)


# 获取信息
def getUserDetail(request):
    val = {"user_id": request.COOKIES.get('user_id')}
    user = database.query(request_name='user_id', val=val)[0]
    user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                 "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
    return HttpResponse(json.dumps(user_info), status=200)


# 获取头图
def getUserAvatar(request):
    val = {"avatar_index": request.COOKIES.get('user_id')}
    return HttpResponse(database.query(request_name='avatar', val=val), status=200)


# 更新历史
def updateHistory(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {'user_id': request.COOKIES.get('user_id'), 'song_id': json_data['song_id'], 'last_time': time.time()}
    if database.query(request_name='user_history_exist', val=val):
        database.update(request_name='history', val=val)
    else:
        database.insert(request_name='history', val=val)
    return HttpResponse(status=200)


def getHistory(request):
    val = {'user_id': request.COOKIES.get('user_id')}
    ids = database.query(request_name='user_history', val=val)[:8]
    data = [
        song.getSongById(sid.song_id) for sid in ids
    ]
    return JsonResponse({'items': data}, status=200)


# 获取音乐推荐
def get_recommendations(request):
    MUSIC_MODEL = model_manager.MUSIC_MODEL
    val = {'user_id': request.COOKIES.get('user_id')}

    user_songs = [hi.song_id for hi in database.query(request_name='user_history', val=val)]
    if len(user_songs) == 0:
        data_list = [
            song.getSongById(i[0]) for i in database.query(request_name='most_listened_song', val=None)
        ]
        return JsonResponse({"recommendations": data_list}, status=200)

    merged_recommendations = defaultdict(float)
    for song_id in user_songs:
        if song_id in MUSIC_MODEL:
            for recommended_songid, score in MUSIC_MODEL[song_id]:
                if recommended_songid not in user_songs:
                    merged_recommendations[recommended_songid] += score
    recommendations = sorted(merged_recommendations.items(), key=lambda x: x[1], reverse=True)[:10]
    recommendations = [
        int(i[0]) for i in recommendations
    ]
    if len(recommendations) > 0:
        data_list = [
            song.getSongById(i) for i in recommendations
        ]
        return JsonResponse({"recommendations": data_list}, status=200)
    return HttpResponse('暂无数据', status=404)


# 获取歌手推荐
def get_recommend_singer(request):
    SINGER_MODEL = model_manager.SINGER_MODEL
    val = {'user_id': request.COOKIES.get('user_id')}

    user_songs = [hi.song_id for hi in database.query(request_name='user_history', val=val)]
    if len(user_songs) == 0:
        data = []
        for i in database.query(request_name='most_listened_singer', val=None):
            temp = song.getSingerInfo(i[0])
            data.append({'singer_id': i[0], 'singer_pic': temp[0], 'singer_name': temp[1]})
        return JsonResponse({'data': data}, status=200)

    singer_ids = []
    for songid in user_songs:
        queryda = database.query(request_name='singer_id', val={'song_id': songid})
        if len(queryda) > 0:
            singer_ids.append(queryda[0][0])

    merged_recommendations = defaultdict(float)
    for singer_id in singer_ids:
        if singer_id in SINGER_MODEL:
            for recommended_singer_id, score in SINGER_MODEL[singer_id]:
                if recommended_singer_id not in singer_ids:
                    merged_recommendations[recommended_singer_id] += score
    recommendations = sorted(merged_recommendations.items(), key=lambda x: x[1], reverse=True)[:10]
    recommendations = [
        int(i[0]) for i in recommendations
    ]
    if len(recommendations) > 0:
        data = []
        for i in recommendations:
            temp = song.getSingerInfo(i)
            data.append({'singer_id': i, 'singer_pic': temp[0], 'singer_name': temp[1]})
        return JsonResponse({'data': data}, status=200)
    return HttpResponse('暂无数据', status=404)
