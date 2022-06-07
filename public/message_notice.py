# -*- coding: utf-8 -*-
# @File: message_notice.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2022/2/23  10:52

from typing import TypeVar

import requests

from public.common import logger,reda_conf

T = TypeVar('T')  # 可以是任何类型。

# 读取配置参数
MSG = reda_conf('MSG')
WECHAT_WEBHOOK = MSG.get('WECHAT').get('wechat_webhook')
WECHAT_MOBILE_LIST = MSG.get('WECHAT').get('wechat_mobile_list')
DINGDING_MOBILE_LIST = MSG.get('DINGDING').get('dingding_mobile_list')
DINGDING_WEBHOOK = MSG.get('DINGDING').get('dingding_webhook')


class EnterpriseWeChatNotice:
    """
    企业微信通知 当前只支持文本
    """

    @staticmethod
    def send_txt(content: T, mentioned_mobile_list: list = WECHAT_MOBILE_LIST):
        """
        发送文本消息通知
        :param content:   文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_mobile_list:  手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """

        headers = {"Content-Type": "text/plain"}
        send_url = WECHAT_WEBHOOK
        send_data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_mobile_list": mentioned_mobile_list  # ['@13823190000',''@all]
            }
        }
        try:
            rep = requests.post(url=send_url, headers=headers, json=send_data)
            logger.info('企业微信消息推送成功！', rep.text)
        except Exception as e:
            logger.error('企业微信消息推送失败！', e)


class DingDingNotice:
    """
    钉钉通知 当前只支持文本
    """

    @staticmethod
    def send_txt(content: T, mobile_list: list = DINGDING_MOBILE_LIST, isattall: bool = True):
        """
        发送文本消息通知
        :param content:   文本内容
        :param mobile_list:  手机号列表，提醒手机号对应的群成员(某个成员)
        :param isattall:  是否要@所有人默认是
        :return:
        """

        headers = {'Content-Type': 'application/json;charset=utf-8'}
        send_url = DINGDING_WEBHOOK
        send_data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "at": {
                    "atMobiles": mobile_list,  # 要@对象的手机号
                    "isAtAll": isattall  # 是否要@所有人
                }, }}

        try:
            rep = requests.post(url=send_url, headers=headers, json=send_data)
            logger.info('钉钉消息推送成功！', rep.text)
        except Exception as e:
            logger.error('钉钉微信消息推送失败！', e)

# if __name__ == '__main__':
#     EnterpriseWeChatNotice.send_txt('测试报告完成 ')
#     DingDingNotice.send_txt('测试报告完成 ！')
