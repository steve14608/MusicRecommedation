import json

from django.http import HttpResponse
from django.shortcuts import render
import database
import time


def loginPage(request):
    if request.COOKIES.get('user_id') is None:
        return render(request, 'music/login1.html')
    else:
        return render(request, 'music/main.html')


# 登录
def login(request):
    user = database.query(request_name='user', val=request)
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
    if database.query(request_name='user_account', val=request):
        return HttpResponse(status=403)
    else:
        ti = time.time()
        user = {'user_account': request['user_account'], 'user_password': request['password'], 'user_id': ti}
        database.insert(request_name='user', val=user)
        rep = HttpResponse(content=ti, status=200)
        rep.set_cookie('user_id', ti)
        return rep


# 更新头图
def updateAvatar(request):
    user = database.query(request_name='user_id',val=request)
    val = {'avatar_index':user.user_id,'avatar':request}
    pass


# 更新签名
def updateBio(request):
    database.update('user', request)
    return HttpResponse(status=200);
    pass


# 获取信息
def getUserDetail(request):
    user = database.query(request_name='user_id',val=request)
    user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                 "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
    return HttpResponse(json.dumps(user_info), status=200)


# 获取头图
def getUsetAvatar(request):
    pass


# 更新历史
def updateHistory(request):
    pass
