"""
webapi接口
搜索结果：https://music.163.com/weapi/cloudsearch/get/web?csrf_token=（post）
评论：https://music.163.com/weapi/comment/resource/comments/get?csrf_token=
歌词：https://music.163.com/weapi/song/lyric?csrf_token=
详情（包括音质）：https://music.163.com/weapi/v3/song/detail?csrf_token=
歌曲下载：https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=

iw233网站解析链接
https://iw233.cn/music/?name=コトダマ紬ぐ未来&type=netease

外链：http://music.163.com/song/media/outer/url?id=534544522.mp3

音乐外链播放器：https://music.163.com/outchain/player?type=2&id=473403600&auto=1&height=66
"""

# 这个文件你不需要管


import base64
import codecs
import json
import math
import random
import time

import requests
from crypto.Cipher import AES
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''

var bKB3x = window.asrsea(JSON.stringify(i3x), buU1x(["流泪", "强"]), buU1x(Rg7Z.md), buU1x(["爱心", "女孩", "惊恐", "大笑"]));
            e3x.data = j3x.cr3x({
                params: bKB3x.encText,
                encSecKey: bKB3x.encSecKey
            })


    window.asrsea = d,

    d: {"hlpretag":"<span class="s-fc7">","hlposttag":"</span>","s":"コトダマ紬ぐ未来","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
    e:010001
    f:00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    g:0CoJUm6Qyw8W8jud
        function d(d, e, f, g) {
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }

        function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
'''


class wangyiyun:
    def __init__(self):
        self.e = '010001'
        self.f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g = '0CoJUm6Qyw8W8jud'

    # 获取一个随意字符串，length是字符串长度
    def generate_str(self, lenght):
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for i in range(lenght):
            index = random.random() * len(str)  # 获取一个字符串长度的随机数
            index = math.floor(index)  # 向下取整
            res = res + str[index]  # 累加成一个随机字符串
        return res

    # AES加密获得params
    def AES_encrypt(self, text, key):
        iv = '0102030405060708'.encode('utf-8')  # iv偏移量
        text = text.encode('utf-8')  # 将明文转换为utf-8格式
        pad = 16 - len(text) % 16
        text = text + (pad * chr(pad)).encode('utf-8')  # 明文需要转成二进制，且可以被16整除
        key = key.encode('utf-8')  # 将密钥转换为utf-8格式
        encryptor = AES.new(key, AES.MODE_CBC, iv)  # 创建一个AES对象
        encrypt_text = encryptor.encrypt(text)  # 加密
        encrypt_text = base64.b64encode(encrypt_text)  # base4编码转换为byte字符串
        return encrypt_text.decode('utf-8')

    # RSA加密获得encSeckey
    def RSA_encrypt(self, str, key, f):
        str = str[::-1]  # 随机字符串逆序排列
        str = bytes(str, 'utf-8')  # 将随机字符串转换为byte类型的数据
        sec_key = int(codecs.encode(str, encoding='hex'), 16) ** int(key, 16) % int(f, 16)  # RSA加密
        return format(sec_key, 'x').zfill(256)  # RSA加密后字符串长度为256，不足的补x

    # 获取参数
    def get_params(self, d, e, f, g):
        i = self.generate_str(16)  # 生成一个16位的随机字符串
        # i = 'aO6mqZksdJbqUygP'
        encText = self.AES_encrypt(d, g)
        # print(encText)    # 打印第一次加密的params，用于测试d正确
        params = self.AES_encrypt(encText, i)  # AES加密两次后获得params
        encSecKey = self.RSA_encrypt(i, e, f)  # RSA加密后获得encSecKey
        return params, encSecKey

    # 传入msg和url,获取返回的json数据
    def get_data(self, msg, url):
        encText, encSecKey = self.get_params(msg, self.e, self.f, self.g)  # 获取参数
        params = {
            "params": encText,
            "encSecKey": encSecKey
        }
        re = requests.post(url=url, params=params, verify=False, timeout=3, cookies={
            "MUSIC_U": "00765D4D5E598D7D03E365B04218FF7C1CC4ACD1888B659C58B7653556603B321DA5964B368DA8D03BD29D45AB46BA7261305EE8D11AE9F64F1EE755338C8FCBA44529083FA8F8B4AD7379548C26C7DE4406ED1CBE58B60FFBE1FFE2BA82A8D7A588F4DA0E470B63C0C2D0CF25B9D5535CBE480F86420BA74634F9D6B28EF2CC9C71D00241A99177D0506207C7F0E84623C4779E179D4DA6D4340E5E0C52C49C54C745BD9D3536D9A047C54C6C9877732D038505B4F35E7FD6743907D355A67803A03345B65D5F7969A7DD527ED8BAC15B9224291F5DBFA3A91E7F8BF297A6A10789EF7F435E8D7BA720700AD7C342DE42DE5076AA2A6D5AC55B4D3C7C60785D7AEC7207051F9B23738F60F96CF1C92AD4897FCD0E8F9A2398FD7209D2157BF66172855FD26D6CEB356A76C0B141E1FC48690950D8357F5A6E79DA8E4EA2322678760AC917B3534B6FD5A13B77FA5EC152D953FAE8EFE21C5CD6FE71321451330583959DC2884846240C71E854F06C99D2"})  # 向服务器发送请求
        return re.json()  # 返回结果

    def get_search(self, hlpretag='<span class=\\"s-fc7\\">', hlposttag='</span>', s='', type='1', queryCorrect='false',
                   offset='0', total='true', limit='30', csrf_token=''):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=' + csrf_token
        # c = '[{' + f'"id":"{id}"' + '}]'
        # msg = {
        #     'id': id,
        #     'c': c,
        #     'csrf_token': csrf_token
        # }
        msg = '{' + f'"hlpretag":"{hlpretag}","hlposttag":"{hlposttag}","s":"{s}","type":"{type}"' \
                    f',"queryCorrect":"{queryCorrect}","offset":"{offset}","total":"{total}",' \
                    f'"limit":"{limit}","csrf_token":"{csrf_token}"' + '}'
        return self.get_data(msg, url)
