# -*- coding: utf-8 -*-
# @File: mail.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2022/2/22  13:59

import os
import smtplib
import time
import zipfile
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import PRPORE_TMP
from public.common import logger, reda_conf

# 读取配置参数
EMAIL = reda_conf('MSG').get('EMAIL')
EMAIL_PORT = EMAIL.get('email_port')
EMAIL_HOST = EMAIL.get('email_host')
SEND_EMAIL_PASSWORD = EMAIL.get('send_email_password')
SEND_EMAIL_USERNAME = EMAIL.get('send_email_username')
RECEIVE_EMAIL_USER = EMAIL.get('receive_email_user')


class SendEMail:
    """封装发送邮件类"""

    def __init__(self, host: str = EMAIL_HOST, port: int = EMAIL_PORT, username: str = SEND_EMAIL_USERNAME,
                 paswword: str = SEND_EMAIL_PASSWORD, receive_email_user: list = RECEIVE_EMAIL_USER, ):
        """
        :param host: 邮箱地址
        :param port: 邮箱端口
        :param username: 发送账号
        :param paswword: 发送密码
        :param receive_email_user: 接收账号
        """
        self.host = host
        self.port = port
        self.username = username
        self.paswword = paswword
        self.receive_email_user = receive_email_user

        # 邮箱服务器地址和端口
        self.smtp_s = smtplib.SMTP_SSL(host=self.host, port=self.port)

        # 发送方邮箱账号和授权码
        self.smtp_s.login(user=self.username, password=self.paswword)

    def dir_zip(self, dirpath: str, outname: str = 'report'):
        """
        压缩目录为zip
        :param dirpath:  目前文件夹路径
        :param outname:  保存路径和名称  /test/demo.zip
        :return:  str
        """
        if not os.path.isdir(dirpath):
            return logger.info('压缩文件不是目录！')
        try:
            outpath = os.path.join(PRPORE_TMP, f'{outname + str(int(time.time()))}.zip')  # 存储路径
            zip = zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED)

            for path, dirnames, filenames in os.walk(dirpath):

                # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                fpath = path.replace(dirpath, '')
                for filename in filenames:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            logger.info('压缩成功！', outpath)
            return outpath
        except Exception as e:
            logger.error('压缩失败！', e)

    def send_text(self, content: str, subject: str, content_type: str = 'plain'):
        """
        发送文本邮件
        :param content: 邮件正文
        :param subject: 邮件主题
        :param content_type: 内容格式：'plain' or 'html'
        :return:
        """
        msg = MIMEText(content, _subtype=content_type, _charset="utf8")

        msg["From"] = self.username
        msg["subject"] = subject

        try:
            if isinstance(self.receive_email_user, list):
                for user in self.receive_email_user:
                    msg["To"] = user
                    self.smtp_s.send_message(msg, from_addr=self.username, to_addrs=user)
                    logger.info(user, '邮件已发送')
        except Exception as e:
            logger.error('发送邮件失败！', e)

    def send_file(self, content: str, subject: str, reports_path: str, filename: str,
                  content_type: str = 'plain'):
        """
        发送带文件的邮件
        :param content: 邮件正文
        :param subject: 邮件主题
        :param reports_path: 文件路径
        :param filename: 邮件中显示的文件名称
        :param content_type: 内容格式
        """
        newfilename = filename
        try:
            if os.path.isdir(reports_path):
                new_reports_path = self.dir_zip(reports_path, filename)

                newfilename = new_reports_path.split('/')[-1]
                file_content = open(new_reports_path, "rb").read()
            else:
                file_content = open(reports_path, "rb").read()
        except Exception as e:
            logger.error('读取文件失败！', e)
            raise '读取文件失败'

        msg = MIMEMultipart()

        text_msg = MIMEText(content, _subtype=content_type, _charset="utf8")
        msg.attach(text_msg)

        file_msg = MIMEApplication(file_content)
        file_msg.add_header('content-disposition', 'attachment', filename=newfilename)
        msg.attach(file_msg)

        msg["From"] = self.username
        msg["subject"] = subject

        try:
            if isinstance(self.receive_email_user, list):
                for user in self.receive_email_user:
                    msg["To"] = user
                    self.smtp_s.send_message(msg, from_addr=self.username, to_addrs=user)
                    logger.info(user, '邮件已发送')
        except Exception as e:
            logger.error('发送邮件失败！', e)

    def send_img(self, subject: str, content, filename: str, content_type: str = 'html'):
        '''
        发送带图片的邮件
        :param to_user: 对方邮箱
        :param subject: 邮件主题
        :param content: 邮件正文
        :param filename: 图片路径
        :param content_type: 内容格式
        '''
        subject = subject
        msg = MIMEMultipart('related')
        # Html正文必须包含<img src="cid:imageid" alt="imageid" width="100%" height="100%>
        content = MIMEText(content, _subtype=content_type, _charset="utf8")
        msg.attach(content)
        msg['Subject'] = subject
        msg['From'] = self.username

        try:
            if isinstance(self.receive_email_user, list):
                for user in self.receive_email_user:
                    msg["To"] = user
                    with open(filename, "rb") as file:
                        img_data = file.read()

                        img = MIMEImage(img_data)
                        img.add_header('Content-ID', 'imageid')
                        msg.attach(img)

                        self.smtp_s.sendmail(self.username, user, msg.as_string())
                    logger.info(user, '邮件已发送')

        except Exception as e:
            logger.error('发送邮件失败！', e)

# if __name__ == '__main__':
# # host = 'smtp.163.com'
# # port = '465'
# # username = 'xxx@163.com'
# # password = 'xxxx'  # 密码或授权码
#     e = SendEMail()
#
#     e.send_text('python发送邮件测试', 'python20222')
# e.send_file(['hanwenlu@reda-flight.com'], 'demo项目测试完成已经完成发送报告请查收', 'demo项目测测试结果',
#             '/Users/reda-flight/Desktop/svn/web-ui/output/report_allure', 'testport')
