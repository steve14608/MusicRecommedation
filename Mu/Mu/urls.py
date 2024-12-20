"""
URL configuration for Mu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import user
from . import song

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.page),
    path('login', user.login),
    path('signup', user.signup),
    path('updateAvatar', user.updateAvatar),
    path('updateInfo', user.updateInfo),
    path('getUserDetail', user.getUserDetail),
    path('getUserAvatar', user.getUserAvatar),
    path('updateHistory', user.updateHistory),
    path('getHistory', user.getHistory),
    path('getSongUrl', song.getSongUrl),
    path('getSongCover', song.getSongCover),
    path('getSongLyrics', song.getSongLyrics),
    path('getSong', song.getSong),
    path('getRecommendation', user.get_recommendations),
    path('getRecommendSinger', user.get_recommend_singer),
    path('getSongBySingerId', song.getSongBySingerId),
    path('searchSong',song.searchSong)
]
