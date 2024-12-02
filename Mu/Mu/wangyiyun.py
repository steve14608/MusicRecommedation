import base64
import codecs
import math
import random

import requests
from Crypto.Cipher import AES
from urllib3.exceptions import InsecureRequestWarning


class wangyiyun:
    def __init__(self):
        self.e = '010001'
        self.f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb' \
                 '7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf6952' \
                 '80104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255' \
                 '932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6' \
                 '935b3ece0462db0a22b8e7'
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
            "MUSIC_U": "002C7AFD15620BB32A50081399F98901B5EC68CF3B501"
                       "34AFBA44F8593B322C1C8723A92958A8E44BD996B17BE7"
                       "E15AF1905C0D90763495E5314C8C011D01035AA7526E3F"
                       "40ACBD4D1C799CA17D5507F0C95D32E99E955DCF02AFD4C"
                       "8D3CE6778CD5E9A50E3D1410D5423FC7AE7BE1043E62FEE"
                       "88582C700EEE152BC368F1374AD82FDC6E7140A6DC7DE15"
                       "9F81CCF7500F272F122ADA4B3D39DBE59A5381FB83CDADC"
                       "8002DA63806C61A395E51FAA1F6318FCED59125995ECBA95"
                       "4B9855E08CD29885632314618E32579223362C9FAB1B1137"
                       "6CED50FF4D4E1142E11E7E8ACEFF580674C078ACE106D0E2"
                       "A217284FF335B6FFDCEBC64F3FC1472BF5343DFD59B6B9C82"
                       "81415E2DB49EC5A4DC332BFAFD1E2D12EA0A8A3FDB1046E5A"
                       "7EC112C4ED852417E892ACFFEC1184B61B83C6C73626D19982"
                       "53858DBE9D345B48719AE9D987938C2122D472EB9C9B3E27E"
                       "4DAC41994965C752DC19CB8CF7CFCEF66295F155AC592AB852"
                       "FC518914A7ECBB0D368562"})

        return re.json()  # 返回结果

    # 返回搜索数据
    def get_search(self, hlpretag='<span class=\\"s-fc7\\">', hlposttag='</span>', s='', type='1', queryCorrect='false',
                   offset='0', total='true', limit='30', csrf_token=''):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=' + csrf_token
        msg = '{' + f'"hlpretag":"{hlpretag}","hlposttag":"{hlposttag}","s":"{s}","type":"{type}"' \
                    f',"queryCorrect":"{queryCorrect}","offset":"{offset}","total":"{total}",' \
                    f'"limit":"{limit}","csrf_token":"{csrf_token}"' + '}'
        return self.get_data(msg, url)