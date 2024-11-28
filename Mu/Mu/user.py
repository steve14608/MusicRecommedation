import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . import database
import time
import os


# 初始界面.判断有没有cookie来确定是去登录界面还是主页面
def page(request):
    if request.COOKIES.get('user_id') is None:
        return redirect(loginPage)
    else:
        temp = database.query(request_name='user_id', val={'user_id': request.COOKIES.get('user_id')})
        if len(temp) == 0:
            request.delete_cookie('user_id')
            return redirect(loginPage)
        return redirect(mainPage)


def loginPage(request):
    if request.COOKIES.get('user_id') is not None:
        redirect(page)
    return render(request, 'login.html')


def mainPage(request):
    if request.COOKIES.get('user_id') is None:
        redirect(page)
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


def get_recommendations(request):
    """
    根据用户的听歌记录生成推荐。
    """
    global MODEL  # 使用全局加载的模型

    # 获取用户的听歌记录（例如通过 POST 提交的 JSON 数据）
    user_data = request.POST.getlist("user_history")  # 假设发送的是歌曲 ID 列表
    user_songs = [int(song_id) for song_id in user_data]

    # 使用模型生成推荐（假设 MODEL 是一个 ItemCF 模型）
    recommendations = []
    for song_id in user_songs:
        if song_id in MODEL:
            recommendations.extend(sorted(MODEL[song_id].items(), key=lambda x: -x[1])[:5])

    # 返回 JSON 响应
    return JsonResponse({"recommendations": recommendations})
