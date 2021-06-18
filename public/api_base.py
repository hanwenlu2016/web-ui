# -*- coding: utf-8 -*-
# @File: api_base.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/17  10:42


from urllib3 import encode_multipart_formdata
import json

import requests

from public.logs import logger
from config.setting import API_URL, TIMEOUT, HEADERS
from public.yaml_data import GetCaseYmal
from public.common import ErrorExcep


class ApiBase:

    def __init__(self):
        self.url = API_URL
        self.headers = HEADERS
        self.timeout = TIMEOUT

    def gourl(self, urlpath):
        """
        判断url
        :param urlpath:  url路径
        :return:
        """
        if urlpath is not None:
            if ('http' or 'https') in urlpath:
                return urlpath
            else:
                return self.url + urlpath

    def post(self, urlpath, params, filePath=None, filename=None, verify=False):
        """
        post 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :return:
        """
        url = self.gourl(urlpath)
        logger.info(f'当前请求接口: {url} ,请求类型: POST')

        try:
            if params is not None and filePath is not None:
                # 处理文件上传
                params['file'] = (filename, open(filePath, 'rb').read())
                encode_data = encode_multipart_formdata(params)
                params = encode_data[0]
                self.headers['Content-Type'] = encode_data[1]
                with requests.post(url, data=params, headers=self.headers, timeout=self.timeout,
                                   verify=verify) as rep:
                    return rep

            with requests.post(url, json=params, headers=self.headers, timeout=self.timeout, verify=verify) as rep:
                return rep
        except Exception as e:
            logger.error(f'请求异常，异常原因:{e}')

    def get(self, urlpath, params=None, verify=False):
        """
        get 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :return:
        """
        url = self.gourl(urlpath)

        logger.info(f'当前请求接口: {url} ,请求类型: GET')

        try:
            if params is not None:
                with requests.get(url, params=json.dumps(params), headers=self.headers, imeout=self.timeout,
                                  verify=verify) as rep:
                    return rep
            with requests.get(url, headers=self.headers, timeout=self.timeout, verify=verify) as rep:
                return rep

        except Exception as e:
            logger.error(f'请求异常，异常原因:{e}')

    def put(self, urlpath, params=None, verify=False):
        """
        put 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :return:
        """
        url = self.gourl(urlpath)
        logger.info(f'当前请求接口{url} ,请求类型: PUT')

        try:
            if params is not None:
                with requests.put(url, data=json.dumps(params), headers=self.headers, timeout=self.timeout,
                                  verify=verify) as rep:
                    return rep
            else:
                logger.warning('put方法必须传递参数！！')

        except Exception as e:
            logger.error(f'请求异常，异常原因:{e}')

    def delete(self, urlpath, verify=False):
        """
        delete 请求
        :param urlpath:  url 路径
        :param verify:   https 请求时忽略证书
        :return:
        """
        url = self.gourl(urlpath)
        logger.info(f'当前请求接口: {url} ,请求类型: DELETE')

        try:
            with requests.delete(url, headers=self.headers, timeout=self.timeout, verify=verify) as rep:
                return rep
        except Exception as e:
            logger.error(f'请求出错，出错原因:{e}')


def apiexe(yamlfile, case, params=None,  verify=True):
    """
    api 请求执行函数
    :param yamlfile:  yaml 文件
    :param case:  用例
    :param params:  请求参数
    :param filePath:  请求文件路径
    :param filename:  上传文件名称
    :param verify:  忽略https
    :return:
    """

    api = ApiBase()
    yaml_data = GetCaseYmal(yaml_name=yamlfile, case_name=case)
    requests_type = yaml_data.reqtype().upper()
    requests_url = yaml_data.urlpath()


    filepath = params.get('filepath') # 临时接收传递数据主要 处理 filepath filename
    filename = params.get('filename')

    # 传递参数时 移除多余参数参数
    if params is not None and ("assertion" in params or "filename" in params or "filepath" in params):
        try:
            del params["assertion"]
            del params["filename"]
            del params["filepath"]
        except Exception:
            pass

    # 判断请求类型是否支持
    if requests_type not in ('POST', 'GET', 'PUT', 'DELETE'):
        raise ErrorExcep('请求类型不支持！！！')

    if requests_type == 'POST':
        return api.post(requests_url, params, filePath=filepath, filename=filename, verify=verify)

    elif requests_type == 'GET':
        return api.get(requests_url, params, verify=verify)

    elif requests_type == 'PUT':
        return api.put(requests_url, params, verify=verify)

    elif requests_type == 'DELETE':
        return api.delete(requests_url, verify=verify)
    else:
        raise ErrorExcep(f'暂时不支持请求类型{requests_type}！！！')

# a = ApiBase()
# a.apiexe('/Users/reda-flight/Desktop/svn/reda-ui-auto/database/locatorYAML/http.yaml', 'post_login')
# if __name__ == '__main__':
#     a = ApiBase()
#     d = {
#         "username": "root",
#         "password": "root"
#     }
#
#     a.post('/login', d)
