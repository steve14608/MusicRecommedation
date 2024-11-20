import json

from django.http import HttpResponse
import database
import time


# 登录
def login(request):
    user = database.query(request_name='user', val=request)
    if user is not None:
        user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                     "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
        return HttpResponse(json.dumps(user_info), status=200)
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
        database.insert(request_name='user', val=request)
        return HttpResponse(content=ti, status=200)


# 更新头图
def updateAvatar(request):
    pass


# 更新签名
def updateBio(request):
    pass


# 获取信息
def getUserDetail(request):
    user = database.query(request_name='user_id')
    user_info = {'user_id': user.user_id, "user_bio": user.user_bio,
                 "user_nickname": user.user_nickname, "user_avatar": user.user_avatar}
    return HttpResponse(json.dumps(user_info), status=200)


# 获取头图
def getUsetAvatar(request):
    pass


# 更新历史
def updateHistory(request):
    pass
