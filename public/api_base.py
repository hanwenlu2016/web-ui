# -*- coding: utf-8 -*-
# @File: api_base.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/6/17  10:42

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

    def post(self, urlpath, params, verify=False):
        """
        post 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :return:
        """
        if ('http' or 'https') in urlpath:
            self.url = urlpath
        else:
            self.url = self.url + urlpath
        logger.info(f'当前请求接口: {self.url} ,请求类型: POST')

        try:
            if params is not None:
                with requests.post(self.url, data=json.dumps(params), headers=self.headers,
                                   timeout=self.timeout,
                                   verify=verify) as rep:
                    return rep

            with requests.post(self.url, data=json.dumps(params), headers=self.headers, timeout=self.timeout,
                               verify=verify) as rep:
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
        if ('http' or 'https') in urlpath:
            self.url = urlpath
        else:
            self.url = self.url + urlpath

        logger.info(f'当前请求接口: {self.url} ,请求类型: GET')

        try:
            if params is not None:
                with requests.get(self.url, params=json.dumps(params), headers=self.headers,
                                  timeout=self.timeout,
                                  verify=verify) as rep:
                    return rep

            with requests.get(self.url, headers=self.headers, timeout=self.timeout,
                              verify=verify) as rep:
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
        if ('http' or 'https') in urlpath:
            self.url = urlpath
        else:
            self.url = self.url + urlpath
        logger.info(f'当前请求接口{self.url} ,请求类型: GET')

        try:
            if params is not None:
                with requests.put(self.url, data=json.dumps(params), headers=self.headers,
                                  timeout=self.timeout,
                                  verify=verify) as rep:
                    return rep

            with requests.put(self.url, headers=self.headers, timeout=self.timeout,
                              verify=verify) as rep:
                return rep

        except Exception as e:
            logger.error(f'请求异常，异常原因:{e}')

    def delete(self, urlpath, params=None, verify=False):
        """
        delete 请求
        :param urlpath:  url 路径
        :param params:  传递参数
        :param verify:   https 请求时忽略证书
        :return:
        """
        if ('http' or 'https') in urlpath:
            self.url = urlpath
        else:
            self.url = self.url + urlpath
        logger.info(f'当前请求接口: {self.url} ,请求类型: DELETE')

        try:
            if params is not None:
                with requests.delete(self.url, params=json.dumps(params), headers=self.headers,
                                     timeout=self.timeout,
                                     verify=verify) as rep:
                    return rep

            with requests.delete(self.url, headers=self.headers, timeout=self.timeout,
                                 verify=verify) as rep:
                return rep
        except Exception as e:
            logger.error(f'请求出错，出错原因:{e}')


def apiexe(yamlfile, case, params=None, verify=True):
    """
    api 请求执行参数
    :param yamlfile:  yaml路径
    :param case:  用例
    :param params:  测试参数
    :param verify:  https 请求时忽略证书
    :return:
    """
    api = ApiBase()
    yaml_data = GetCaseYmal(yaml_name=yamlfile, case_name=case)
    requests_type = yaml_data.reqtype().upper()
    requests_url = yaml_data.urlpath()

    # 传递参数时 移除断言参数
    if params is not None and "assertion" in params:
        del params["assertion"]

    # 判断请求类型是否支持
    if requests_type not in ('POST', 'GET', 'PUT', 'DELETE'):
        raise ErrorExcep('请求类型不支持！！！')

    if requests_type == 'POST':
        return api.post(requests_url, params, verify=verify)

    elif requests_type == 'GET':
        return api.get(requests_url, params, verify=verify)

    elif requests_type == 'PUT':
        api.put(requests_url, params, verify=verify)

    elif requests_type == 'DELETE':
        api.delete(requests_url, params, verify=verify)
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
