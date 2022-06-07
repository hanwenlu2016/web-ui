# -*- coding: utf-8 -*-
# @File: common.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/1  16:11

import os
import re
import shutil
import sys
import time
from typing import TypeVar, Tuple

import cv2
import numpy as np
import yaml
from loguru import logger

from config import PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR, LOG_DIR, DIFF_IMGPATH, STETING_YAML_DIR

# import ddddocr 不支持Python3.10
# 可以是任意类型


T = TypeVar('T')


def reda_conf(value: str) -> list or dict or str:
    """
    读取yaml配置文件
    :param value: 读取的建
    :return:
    """
    try:
        with open(STETING_YAML_DIR, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            for da in data:
                if da.get(value) is not None:
                    return da.get(value)
    except Exception as e:
        logger.error(f'读取yaml异常{e}')


levels = reda_conf('CURRENCY').get('LEVEL')  # 读取配置



def find_dict(will_find_dist: dict, find_keys: T) -> list or int:
    """
    查询 嵌套字典中的值
    :param will_find_dist:  要查找的字典
    :param find_keys:  要查找的key
    :return:  list
    """

    value_found = []
    if (isinstance(will_find_dist, (list))):  # 含有列表的值处理
        if (len(will_find_dist) > 0):
            for now_dist in will_find_dist:
                found = find_dict(now_dist, find_keys)
                if (found):
                    value_found.extend(found)
            return value_found

    if (not isinstance(will_find_dist, (dict))):  # 没有字典类型的了
        return 0

    else:  # 查找下一层
        dict_key = will_find_dist.keys()
        for i in dict_key:
            if (i == find_keys):
                value_found.append(will_find_dist[i])
            found = find_dict(will_find_dist[i], find_keys)
            if (found):
                value_found.extend(found)

        return value_found


def is_assertion(dicts: T, actual: T) -> None:
    """
    断言参数
    :param dicts: dict 断言参数
    :param actual: 实际结果
    :return:
    """

    if dicts is not None:
        is_assertion_results(actual=actual, expect=dicts[-2], types=dicts[-1])


def is_assertion_results(actual: T, expect: T, types: str) -> bool:
    """
    断言函数
    :param actual: 实际结果
    :param expect:  预期结果
    :param types:  断言类型    ==(等于) !=(不等于) in(包含) notin(不包含)
    :return:
    """
    if isinstance(actual, dict):
        if isinstance(expect, dict):
            actual = find_dict(actual, list(expect)[0])  # 利用字典的键获取断言的值
            expect = list(expect.values())[0]
    if types == '==':
        assert expect == actual
        return True

    elif types == '!=':
        assert expect != actual
        return True

    elif types == 'in':
        assert expect in actual
        return True

    elif types == 'notin':
        assert expect not in actual
        return True

    elif types == None:
        return False
    else:
        logger.error('输入的类型不支持！！')
        return False


# 提取字符中的整数
def extract_str_in_int(string: str) -> list:
    """
    提取字符中的整数
    :param string: 字符串
    :return: list
    """
    findlist = re.findall(r'[1-9]+\.?[0-9]*', string)
    return findlist


# 自定义异常类
class ErrorExcep(Exception):
    """
    自定义异常类
    """

    def __init__(self, message):
        super().__init__(message)


# 日志设置类
class SetLog:
    """
    日志设置类  使用 logger 请从此logs目录导入
    """

    DAY = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    LOG_PATH = os.path.join(LOG_DIR, f'{DAY}_all.log')

    ERR_LOG_PATH = os.path.join(LOG_DIR, f'{DAY}_err.log')

    logger.add(LOG_PATH, rotation="00:00", encoding='utf-8')

    logger.add(ERR_LOG_PATH, rotation="00:00", encoding='utf-8', level='ERROR', )
    logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象

    handler_id = logger.add(sys.stderr, level=levels)  # 添加一个可以修改控制的handler


# 删除测试报告
class DelReport:

    def mkdir(self, path: str) -> None:
        """
        文件夹不存在就创建
        :param path:
        :return:
        """
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        else:
            pass

    def clean_report(self, filepath: str) -> None:
        """
        清除测试报告文件
        :param filepath:  str  清除路径
        :return:
        """
        del_list = os.listdir(filepath)
        if del_list:
            try:
                for f in del_list:
                    file_path = os.path.join(filepath, f)

                    # 判断是不是文件
                    if os.path.isfile(file_path):
                        if not file_path.endswith('.xml'):  # 不删除.xml文件
                            os.remove(file_path)
                    else:
                        os.path.isdir(file_path)
                        shutil.rmtree(file_path)
            except Exception as e:
                logger.error(e)

    def run_del_report(self, ) -> None:
        """
        执行删除测试报告记录
        :return:
        """
        is_clean_report = reda_conf('CURRENCY').get('IS_CLEAN_REPORT')
        if is_clean_report == True:  # 如果为 True 清除 PRPORE_ALLURE_DIR、 PRPORE_JSON_DIR 、PRPORE_SCREEN_DIR 路径下报告

            try:
                dir_list = [PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR]
                for dir in dir_list:
                    self.mkdir(dir)
                    self.clean_report(dir)
                logger.info('清除测试报告中.....')
            except Exception as e:
                logger.error(e)

        else:
            logger.warning('清理报告未启用！！')


class AlgorithmClassify:
    """
    图片算法类
    """

    @classmethod
    def aHash(cls, img: str) -> str:
        """
        均值哈希算法
        :param img: 图片名称
        :return:
        """

        # 缩放为8*8
        img = cv2.resize(img, (8, 8))
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    @classmethod
    def dHash(cls, img: str) -> str:
        """
        差值感知算法
        :param img:  图片名称
        :return:
        """
        # 缩放8*8
        img = cv2.resize(img, (9, 8))
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    @classmethod
    def pHash(cls, img: str) -> list:
        """
        感知哈希算法(pHash)
        :param img:  图片名称
        :return:
        """
        # 缩放32*32
        img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 将灰度图转为浮点型，再进行dct变换
        dct = cv2.dct(np.float32(gray))
        # opencv实现的掩码操作
        dct_roi = dct[0:8, 0:8]

        hash = []
        avreage = np.mean(dct_roi)
        for i in range(dct_roi.shape[0]):
            for j in range(dct_roi.shape[1]):
                if dct_roi[i, j] > avreage:
                    hash.append(1)
                else:
                    hash.append(0)
        return hash

    @classmethod
    def calculate(cls, image1: str, image2: str) -> str:
        """
         计算单通道的直方图的相似值
        :param image1:
        :param image2:
        :return:
        """
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree


class ImgDiff:
    """
    图片对比运用类
    图片算法对比  推荐 差值哈希算法/ahaDiff
    """

    @classmethod
    def sampleIMG(CLS, imgname: str) -> str:
        """
        * 样本数据 检查与路径返回
        返回img测试图片路径  * 断言图片时使用
        :param imgname: imgname 图片名称 默认png格式
        :return:
        """

        # 获取准备测试图片路径的名称
        img_list = [i[2] for i in os.walk(DIFF_IMGPATH)]

        if imgname not in img_list[0]:
            logger.error('样本图片不存在')
            raise ErrorExcep('样本图片不存在')
        return os.path.join(DIFF_IMGPATH, f"{imgname}")

    @classmethod
    def cmpHash(cls, hash1: str, hash2: str) -> int:
        """
        Hash值对比函数
        :param hash1: 哈希值1
        :param hash2: 哈希值2
        :return:
        """
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            return -1
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] != hash2[i]:
                n = n + 1
        return n

    @classmethod
    def classify_hist_with_split(cls, image1: str, image2: str, size: Tuple[str] = (256, 256)) -> float:
        """
        通过得到RGB每个通道的直方图来计算相似度
         将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        :param image1: 图片1 样本数据
        :param image2: 图片2 需要对比的图片
        :param size:
        :return:
        """
        image1 = cv2.resize(cv2.imread(cls.sampleIMG(image1)), size)
        image2 = cv2.resize(cv2.imread(image2), size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += AlgorithmClassify.calculate(im1, im2)
        sub_data = sub_data / 3
        logger.debug(f'三直方图算法相似度:{sub_data}')
        return sub_data

    @classmethod
    def ahaDiff(cls, img1: str, img2: str) -> int:
        """
        均值哈希算法对比
        :param img1: 图片1  样本数据
        :param img2: 图片2  需要对比的数据
        :return:
        """
        img1 = cls.sampleIMG(img1)  # 获取样本数据路径
        try:
            hash1 = AlgorithmClassify.aHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.aHash(cv2.imread(img2))
            n = cls.cmpHash(hash1, hash2)
            logger.debug(f'均值哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比均值哈希错误:{e}')

    @classmethod
    def dhaDiff(cls, img1: str, img2: str) -> int:
        """
        差值哈希算法对比
        :param img1: 图片1 样本数据
        :param img2: 图片2 需要对比的数据
        :return:
        """
        img1 = cls.sampleIMG(img1)  # 获取样本数据路径
        try:
            hash1 = AlgorithmClassify.dHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.dHash(cv2.imread(img2))
            n = cls.cmpHash(hash1, hash2)
            logger.debug(f'差值哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比差值哈希错误:{e}')

    @classmethod
    def phaDiff(cls, img1: str, img2: str) -> int:
        """
        感知哈希算法对比
        :param img1: 图片1 样本数据
        :param img2: 图片2 需要对比的数据
        :return:
        """
        img1 = cls.sampleIMG(img1)  # 获取样本数据路径
        try:
            hash1 = AlgorithmClassify.pHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.pHash(cv2.imread(img2))
            n = cls.cmpHash(str(hash1), str(hash2))
            logger.debug(f'感知哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比差感知哈希错误:{e}')

# def read_img_verification_code(image: str):
#     """
#     读取图片验证码 借助 ddddocr 此库相对识别高 https://github.com/sml2h3/ddddocr
#     :param image: 图片验证码
#     :return: str
#     """
#     try:
#         img_ocr = ddddocr.DdddOcr(show_ad=False)
#         res = img_ocr.classification(image)
#         logger.info(f'识别验证码成功：{res}')
#         return res
#     except Exception as e:
#         logger.error(e, '读取验证码异常！')

#
# d = ImgDiff.dhaDiff('test.png1',
#                     r'/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/test_login_1624331940125.png')
#
# print(d)
# if __name__ == '__main__':
#     l=reda_conf('CURRENCY').get('LEVEL')
#     print(l)
