# -*- coding: utf-8 -*-
# @File: common.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/2/1  16:11

import os, sys, time
import re
import shutil
import os
import cv2

import numpy as np
from loguru import logger

from config.setting import IS_CLEAN_REPORT, LEVEL
from config.ptahconf import PRPORE_ALLURE_DIR, PRPORE_JSON_DIR, PRPORE_SCREEN_DIR, LOG_DIR, DIFF_IMGPATH


def is_assertion(expect, actual, types):
    """
    断言参数
    :param expect: 预期
    :param actual: 实际
    :param types: 断言类型
    :return:
    """
    if types == '==':
        assert expect == actual
    elif types == '!=':
        assert expect != actual
    elif types == 'in':
        assert expect in actual
    elif types == 'notin':
        assert expect not in actual
    elif types == None:
        pass
    else:
        logger.error('输入的类型不支持！！')


def facename(func):
    """
    获取函数名称 *装饰器
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        name = func.__name__
        return name

    return wrapper


def ymal(*args, **kwargs):
    """
    装饰器
    获取当前运行文件的py文件并转为yaml
    :param args:
    :param kwargs:
    :return:
    """

    def getyaml(func):
        def yaml():
            # name=func.__name__
            yamlfile = args[0](__file__).name.replace('py', 'yaml')
            return yamlfile  # ,name

        return yaml

    return getyaml


# 获取运行函数名称
def get_run_func_name():
    """
    获取运行函数名称
    :return:
    """
    try:
        raise Exception
    except:
        exc_info = sys.exc_info()
        traceObj = exc_info[2]
        frameObj = traceObj.tb_frame
        Upframe = frameObj.f_back
        return Upframe.f_code.co_name


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

    logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
    
    logger.add(LOG_PATH, rotation="00:00", encoding='utf-8')

    logger.add(ERR_LOG_PATH, rotation="00:00", encoding='utf-8', level='ERROR', )
    
    handler_id = logger.add(sys.stderr, level=LEVEL)  # 添加一个可以修改控制的handler


# 删除测试报告
class DelReport:

    def mkdir(self, path):
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
        if IS_CLEAN_REPORT == True:  # 如果为 True 清除 PRPORE_ALLURE_DIR、 PRPORE_JSON_DIR 、PRPORE_SCREEN_DIR 路径下报告

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
    def sampleIMG(CLS, imgname):
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
    def classify_hist_with_split(cls, image1: str, image2: str, size=(256, 256)) -> float:
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

#
# d = ImgDiff.dhaDiff('test.png1',
#                     r'/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/test_login_1624331940125.png')
#
# print(d)
