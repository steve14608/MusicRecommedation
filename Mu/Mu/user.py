import json

from django.http import HttpResponse
from django.shortcuts import render
import database
import time


# 初始界面.判断有没有cookie来确定是去登录界面还是主页面
def page(request):
    if request.COOKIES.get('user_id') is None:
        return render(request, 'music/login1.html')
    else:
        return render(request, 'music/main.html')


# 登录
def login(request):
    val = {"user_account": request['user_account'], "user_password": request['user_password']}
    user = database.query(request_name='user', val=val)
    if user is not None:
        user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                     "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
        rep = HttpResponse(json.dumps(user_info), status=200)
        rep.set_cookie('user_id', user.user_id)
        return rep
    else:
        return HttpResponse(status=403)
    pass


# 注册
def signup(request):
    val = {"user_account": request['user_account'], "user_password": request['user_password']}
    if database.query(request_name='user_account', val=val):
        return HttpResponse(status=403)
    else:
        ti = time.time()
        user = {'user_account': val['user_account'], 'user_password': val['password'], 'user_id': ti, 'user_avatar': ti,
                'user_bio': '无', 'user_nickname': '默认'}
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


# 更新签名
def updateBio(request):
    val = {'user_id': request.COOKIES.get('user_id'), 'user_bio': request['bio']}
    database.update('user', val)
    return HttpResponse(status=200)


# 获取信息
def getUserDetail(request):
    user = database.query(request_name='user_id', val=request)
    user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                 "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
    return HttpResponse(json.dumps(user_info), status=200)


# 获取头图
def getUsetAvatar(request):
    val = {"avatar_index": request.COOKIES.get('user_id')}
    return HttpResponse(database.query(request_name='avatar', val=val), status=200)


# 更新历史
def updateHistory(request):
    val = {'user_id': request.COOKIES.get('user_id'), 'song_id': request['song_id'], 'last_time': time.time()}
    database.update(request_name='history', val=val)
    return HttpResponse(status=200)
