from django.http import HttpResponse, JsonResponse
from . import database
import json
import os
import urllib.parse
from hashlib import md5
from random import randrange
import requests
from .wangyiyun import wangyiyun
from lxml import etree
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# 前端搜索的功能
def searchSong(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {"song_name": json_data['search']}

    # data_list = database.query('song_name', val)  # 列表，每个列表都是一个元组
    data = wangyiyun().get_search(s=val['song_name'])
    song_list = [
        {'song_id': i['id'], 'song_name': i['name'], 'song_singer': i['ar'][0]['name'],
         'song_singer_id': i['ar'][0]['id'], 'song_album': i['al']['name'], 'song_duration': i['dt']}
        for i in data['result']['songs'][:10]
    ]
    return JsonResponse({'data': song_list}, status=200)



# 根据song_id返回file
def getSongUrl(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)

    jsondata = str(json_data['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    # song_file = save_cache(uid=0, val=urlv1['data'][0]['url'], filetype='mp3')
    return HttpResponse(urlv1['data'][0]['url'], status=200)


# 根据歌曲id返回歌曲图片
def getSongCover(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)

    jsondata = str(json_data['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    namev1 = name_v1(urlv1['data'][0]['id'])
    # cover_file = save_cache(uid=0, val=namev1['songs'][0]['al']['picUrl'], filetype='jpg')
    return HttpResponse(namev1['songs'][0]['al']['picUrl'], status=200)


# 根据歌曲id返回歌词
def getSongLyrics(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    print(json_data)
    jsondata = str(json_data['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    lyricv1 = lyric_v1(urlv1['data'][0]['id'], cookies)
    return JsonResponse({'lyric':lyricv1['lrc']['lyric']})


# 返回歌曲封面、作者、歌名
def getSong(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)

    jsondata = str(json_data['song_id'])
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    namev1 = name_v1(urlv1['data'][0]['id'])

    jsdata = {'song_name': namev1['songs'][0]['name'], 'singer': namev1['songs'][0]['ar'][0]['name'],
              'cover': namev1['songs'][0]['al']['picUrl']}
    return JsonResponse(jsdata, status=200)


def getSongById(sid):
    jsondata = str(sid)
    cookies = parse_cookie(read_cookie())
    urlv1 = url_v1(ids(jsondata), 'standard', cookies)
    namev1 = name_v1(urlv1['data'][0]['id'])

    return {'song_name': namev1['songs'][0]['name'], 'singer': namev1['songs'][0]['ar'][0]['name'],
            'cover': namev1['songs'][0]['al']['picUrl'],'song_id':sid}


def getSongBySingerId(request):
    raw_data = request.body.decode("utf-8")
    json_data = json.loads(raw_data)
    val = {'song_singer_id': json_data['song_singer_id']}
    data = database.query(request_name='song_singer_id', val=val)  # songinfo的list
    if len(data) < 4:
        da = getSingerSongInfo(val['song_singer_id'])
    else:
        da = [
            {'song_id': i.song_id, 'song_name': i.song_name} for i in data
        ]
    return JsonResponse({'singer_name': data[0].song_singer, 'singer_id': data[0].song_singer_id, 'data': da},
                        status=200)


def getSingerHeadPic(singer_id):
    html = etree.HTML(
        requests.get(url=f'https://music.163.com/artist?id={singer_id}', headers={'User-Agent': 'Mozilla/5.0 (Windows '
                                                                                                'NT 10.0;'
                                                                                                'Win64; x64) '
                                                                                                'AppleWebKit/537.36 ('
                                                                                                'KHTML, like Gecko) '
                                                                                                'Chrome/131.0.0.0 '
                                                                                                'Safari/537.36'
                                                                                                'Edg/131.0.0.0'}).content)
    return html.xpath("//div[@class='n-artist f-cb']/img/@src")[0]


def getSingerSongInfo(singer_id):
    html = etree.HTML(
        requests.get(url=f'https://music.163.com/artist?id={singer_id}', headers={'User-Agent': 'Mozilla/5.0 (Windows '
                                                                                                'NT 10.0;'
                                                                                                'Win64; x64) '
                                                                                                'AppleWebKit/537.36 ('
                                                                                                'KHTML, like Gecko) '
                                                                                                'Chrome/131.0.0.0 '
                                                                                                'Safari/537.36'
                                                                                                'Edg/131.0.0.0'}).content)
    datalist = []
    lista = html.xpath("//ul[@class='f-hide']/li/a/@href")
    listb = html.xpath("//ul[@class='f-hide']/li/a").text
    for i in range(0, len(lista) if len(lista) < 10 else 10):
        datalist.append({'song_id': lista[i][9:], 'song_name': listb[i]})
    return datalist


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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 '
                      'Chrome/91.0.4472.164 NeteaseMusicDesktop/2.10.2.200154',
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
