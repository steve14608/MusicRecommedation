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

            "MUSIC_U": "004C43CC0216A157A4C4761D4F800B05167C0E68636059D849AD751366"
                       "2107EED95CE09CD95BA65880A693DFFD152EF0B677966BFC1FB0C9B453"
                       "A03970B1507D29FE96EEE171AAA7B1AA0BEFA606CA0F333D3D835F057F"
                       "0088474DAF0C40D68D996AB5CDFAB0A26B47C832DF5A21BF197598D0D5"
                       "D23AFC60C69AD617FB52CA907C57CF1BAFBA333B013DEBE571ABF04D6A"
                       "6E8503E3C9C6283430E1C8CC07DDA23D7D3AC7D69A15ACA350584F982A"
                       "0804DCB69B9C224F3ADCF5F59BDD06A8260C31AC7ED575F15DFC279E6C"
                       "79A5FE50C850AA2477F8A87D1A6584F4317BA1935EFD56CEBD50FB9E1C"
                       "057D9208AD490EFDA9501E72A0122A06D94965EACB72A542FCA64855ED"
                       "1D70580891CBBF39A64351EC43402B1A472A84B30CB321DF8961678044"
                       "DE08CC42832E9F0628F3E6AE3B159BE29DEBACC6FB42E5D25C8866AE1B"
                       "487472081235C3111DE0913D93C470353A8974E2D3565B97E051E3D450"
                       "CAE9426ACBC3AAD8A21DC6A1A7927B58DFC7BB6F56"})
        return re.json()  # 返回结果

    # 返回搜索数据
    def get_search(self, hlpretag='<span class=\\"s-fc7\\">', hlposttag='</span>', s='', type='1', queryCorrect='false',
                   offset='0', total='true', limit='30', csrf_token=''):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=' + csrf_token
        msg = '{' + f'"hlpretag":"{hlpretag}","hlposttag":"{hlposttag}","s":"{s}","type":"{type}"' \
                    f',"queryCorrect":"{queryCorrect}","offset":"{offset}","total":"{total}",' \
                    f'"limit":"{limit}","csrf_token":"{csrf_token}"' + '}'
        return self.get_data(msg, url)


    def get_data_no_cookie(self, msg, url):
        encText, encSecKey = self.get_params(msg, self.e, self.f, self.g)  # 获取参数
        params = {
            "params": encText,
            "encSecKey": encSecKey
        }
        re = requests.post(url=url, params=params, verify=False, timeout=3)
        return re.json()

    def getSongInfo(self, song_id, csrf_token=''):
        msg = '{' + f'"id":"{song_id}",' + r'"c":"[{\"id\":\"' + str(
            song_id) + r'\"}]",' + f'"csrf_token":"{csrf_token}"' + '}'

        url = f'https://music.163.com/weapi/v3/song/detail?csrf_token={csrf_token}'
        return self.get_data_no_cookie(msg, url)
