# -*- coding: utf-8 -*-
# @File: redaimg.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/11/6  13:59


import requests
from hashlib import md5

from config.setting import IMG_INFO


class CjyClient:

    def __init__(self, username, password, soft_id, apiurl):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.apiurl = apiurl
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id, }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def postPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post(self.apiurl, data=params, files=files,
                          headers=self.headers)
        return r.json()


def imgContent(img_path, img_type=1902):
    """
    云打码验证码
    :param img_path: 图片路径
    :param img_type:  图片类型 默认 1902
    :return: str
    """
    '''
    https://www.chaojiying.com/price.html
    1902	常见4~6位英文数字(急速)	
    1101	1位英文数字	
    1004	1~4位英文数字	
    1005	1~5位英文数字	
    1006	1~6位英文数字	
    1007	1~7位英文数字	
    1008	1~8位英文数字	
    1009	1~9位英文数字	
    1010	1~10位英文数字	
    1012	1~12位英文数字	
    1020	1~20位英文数字	
    '''

    rep = CjyClient(IMG_INFO.get('username'), IMG_INFO.get('password'), IMG_INFO.get('code_id'),
                    IMG_INFO.get('api_url'))

    with open(img_path, 'rb') as f:
        im = f.read()
        img_text = rep.postPic(im, img_type)

    return img_text.get('pic_str')
