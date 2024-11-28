from django.http import HttpResponse, JsonResponse
import database
import json
import os
import urllib.parse
from hashlib import md5
from random import randrange
import requests
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Mus import models
from netease import wangyiyun


# 前端搜索的功能
def searchSong(request):
    id_list = database.query('song_name', request['song_name'])
    song_list = []
    single = {}
    if len(id_list) < 2:
        data = wangyiyun().get_search(s=request['song_name'])
        data = data['result']['songs']
        for di in data:
            single['song_id'] = di['id']
            single['song_name'] = di['name']
            single['song_singer'] = di['ar'][0]['name']
            song_list.append(single)
    else:
        for song_id in id_list:
            song_info = database.query('song_info', song_id)
            single['song_id'] = song_info.song_id
            single['song_name'] = song_info.song_name
            single['song_singer'] = song_info.song_singer
            song_list.append(single)
    return json.dumps(song_list)


# 根据song_id返回file
def getSongUrl(response):
    jsondata = str(response['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    # song_file = save_cache(uid=0, val=urlv1['data'][0]['url'], filetype='mp3')
    return HttpResponse(urlv1['data'][0]['url'], status=200)


# 根据歌曲id返回歌曲图片
def getSongCover(response):
    jsondata = str(response['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    namev1 = name_v1(urlv1['data'][0]['id'])
    # cover_file = save_cache(uid=0, val=namev1['songs'][0]['al']['picUrl'], filetype='jpg')
    return HttpResponse(namev1['songs'][0]['al']['picUrl'], status=200)


# 根据歌曲id返回歌词
def getSongLyrics(response):
    jsondata = str(response['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    lyricv1 = lyric_v1(urlv1['data'][0]['id'], cookies)
    return HttpResponse(lyricv1['lrc']['lyric'])


def getSong(response):
    jsondata = str(response['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    namev1 = name_v1(urlv1['data'][0]['id'])

    jsdata = {'song_name': namev1['songs'][0]['name'], 'singer': namev1['songs'][0]['ar'][0]['name'],
              'cover': namev1['songs'][0]['al']['picUrl']}
    return JsonResponse(jsdata)


# 下面的函数都不用看


def HexDigest(data):
    return "".join([hex(d)[2:].zfill(2) for d in data])


def HashDigest(text):
    HASH = md5(text.encode("utf-8"))
    return HASH.digest()


def HashHexDigest(text):
    return HexDigest(HashDigest(text))


def parse_cookie(text: str):
    cookie_ = [item.strip().split('=', 1) for item in text.strip().split(';') if item]
    cookie_ = {k.strip(): v.strip() for k, v in cookie_}
    return cookie_


def read_cookie():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookie_file = os.path.join(script_dir, 'cookie.txt')
    with open(cookie_file, 'r') as f:
        cookie_contents = f.read()
    return cookie_contents


def post(url, params, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/91.0.4472.164 NeteaseMusicDesktop/2.10.2.200154',
        'Referer': '',
    }
    cookies = {
        "os": "pc",
        "appver": "",
        "osver": "",
        "deviceId": "pyncm!"
    }
    cookies.update(cookie)
    response = requests.post(url, headers=headers, cookies=cookies, data={"params": params})
    return response.text


# 输入id选项
def ids(ids):
    if '163cn.tv' in ids:
        response = requests.get(ids, allow_redirects=False)
        ids = response.headers.get('Location')
    if 'music.163.com' in ids:
        index = ids.find('id=') + 3
        ids = ids[index:].split('&')[0]
    return ids


def url_v1(id, level, cookies):
    url = "https://interface3.music.163.com/eapi/song/enhance/player/url/v1"
    AES_KEY = b"e82ckenh8dichen8"
    config = {
        "os": "pc",
        "appver": "",
        "osver": "",
        "deviceId": "pyncm!",
        "requestId": str(randrange(20000000, 30000000))
    }

    payload = {
        'ids': [id],
        'level': level,
        'encodeType': 'flac',
        'header': json.dumps(config),
    }

    if level == 'sky':
        payload['immerseType'] = 'c51'

    url2 = urllib.parse.urlparse(url).path.replace("/eapi/", "/api/")
    digest = HashHexDigest(f"nobody{url2}use{json.dumps(payload)}md5forencrypt")
    params = f"{url2}-36cd479b6b5-{json.dumps(payload)}-36cd479b6b5-{digest}"
    padder = padding.PKCS7(algorithms.AES(AES_KEY).block_size).padder()
    padded_data = padder.update(params.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB())
    encryptor = cipher.encryptor()
    enc = encryptor.update(padded_data) + encryptor.finalize()
    params = HexDigest(enc)
    response = post(url, params, cookies)
    return json.loads(response)


def name_v1(id):
    # 歌曲信息接口
    urls = "https://interface3.music.163.com/api/v3/song/detail"
    data = {'c': json.dumps([{"id": id, "v": 0}])}
    response = requests.post(url=urls, data=data)
    return response.json()


def lyric_v1(id, cookies):
    # 歌词接口
    url = "https://interface3.music.163.com/api/song/lyric"
    data = {'id': id, 'cp': 'false', 'tv': '0', 'lv': '0', 'rv': '0', 'kv': '0', 'yv': '0', 'ytv': '0', 'yrv': '0'}
    response = requests.post(url=url, data=data, cookies=cookies)
    return response.json()
