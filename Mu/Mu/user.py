import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import database
import time
import os


# 初始界面.判断有没有cookie来确定是去登录界面还是主页面
def page(request):
    if request.COOKIES.get('user_id') is None:
        return render(request, 'login1.html')
    else:
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
        ti = time.time()
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
    val = {'user_id': request.COOKIES.get('user_id'), 'avatar': request['avatar']}
    database.update(request_name='avatar', val=val)
    return HttpResponse(status=200)


# 更新签名和昵称
def updateInfo(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {'user_id': request.COOKIES.get('user_id'), 'user_bio': json_data['bio']}
    database.update('user', val)
    return HttpResponse(status=200)


# 获取信息
def getUserDetail(request):
    val = {"user_id": request.COOKIES.get('user_id')}
    user = database.query(request_name='user_id', val=val)
    user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                 "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
    return HttpResponse(json.dumps(user_info), status=200)


# 获取头图
def getUsetAvatar(request):
    val = {"avatar_index": request.COOKIES.get('user_id')}
    return HttpResponse(database.query(request_name='avatar', val=val), status=200)


# 更新历史
def updateHistory(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {'user_id': request.COOKIES.get('user_id'), 'song_id': json_data['song_id'], 'last_time': time.time()}
    database.update(request_name='history', val=val)
    return HttpResponse(status=200)


def getHistory(request):
    val = {'user_id': request.COOKIES.get('user_id')}
    items = database.query(request_name='user_history', val=val)
    data = [
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
        } for item in items
    ]
    return JsonResponse({'items': data})
