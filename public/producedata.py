# -*- coding: utf-8 -*-
# @File: produce_data.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/26  11:19


from faker import Factory

fake = Factory().create('zh_CN')


class PersonalInfo:
    """
    基于 faker 封装个人测试信息类
    """

    @staticmethod
    def random_name():
        """
        随机姓名
        :return: str
        """
        return fake.name()

    @staticmethod
    def random_phone_number():
        """
        随机手机号码
        :return:  int
        """
        return fake.phone_number()

    @staticmethod
    def random_email():
        """
        随机邮箱
        :return:
        """
        return fake.email()

    @staticmethod
    def random_job():
        """
       随机职位
       :return:
       """
        return fake.job()

    @staticmethod
    def random_ssn():
        """
       随机 省份证信息
       :return:
       """
        return fake.ssn(min_age=18, max_age=90)

    @staticmethod
    def random_company():
        """
        随机 公司名
        :return:
        """
        return fake.company()


class AddressInfo:
    """
    基于 faker 封装地址相关测试信息类
    """

    @staticmethod
    def random_city():
        """
        随机 城市
        :return:  str
        """
        return fake.city_name()

    @staticmethod
    def random_province():
        """
        随机 省份
        :return:  str
        """
        return fake.province()

    @staticmethod
    def random_country():
        """
        随机 国家
        :return:  str
        """
        return fake.country()

    @staticmethod
    def random_address():
        """
        随机住址信息
        :return:  str
        """
        return fake.address()


class TimeInfo:
    """
    基于 faker 封装时间信息类
    """

    @staticmethod
    def random_time():
        """
        随机时间24H   22:00:00
        :return: str
        """
        return fake.time()

    @staticmethod
    def random_year():
        """
        随机月份
        :return: str[0] -数字月  str[0] -英文月
        """
        return (fake.month(),fake.month_name())


    @staticmethod
    def random_month():
        """
        随机年份
        :return: str
        """
        return fake.month()


    @staticmethod
    def random_date_this_month():
        """
        随机 本月中的日期时间
        :return: str
        """
        return fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None)

    @staticmethod
    def random_date_this_decade():
        """
        随机 本年中的日期时间
        :return: str
        """
        return fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

    @staticmethod
    def random_date_time_this_century():
        """
        随机 本世纪中的日期和时间
        :return: str
        """
        return fake.date_time_this_century(before_now=True, after_now=False, tzinfo=None)


    @staticmethod
    def random_day_of_week():
        """
        随机星期
        :return:  str
        """
        return fake.day_of_week()

    @staticmethod
    def random_date_of_birth(age):
        """
        随机生日
        :param age:  int  需要随机多少岁之内
        :return:  str
        """
        return fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=age)


