# -*- coding: utf-8 -*-
# @File: imgproce.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/5/10  15:20

import cv2
import numpy as np

from public.logs import logger


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


class Diff:
    """
    图片对比运用类
    图片算法对比  推荐 差值哈希算法/dHash
    """

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
        :param image1: 图片1
        :param image2: 图片2
        :param size:
        :return:
        """
        image1 = cv2.resize(cv2.imread(image1), size)
        image2 = cv2.resize(cv2.imread(image2), size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += AlgorithmClassify.calculate(im1, im2)
        sub_data = sub_data / 3
        logger.info(f'三直方图算法相似度:{sub_data}')
        return sub_data

    @classmethod
    def aHash(cls, img1: str, img2: str) -> int:
        """
        均值哈希算法对比
        :param img1: 图片1
        :param img2: 图片2
        :return:
        """
        try:
            hash1 = AlgorithmClassify.aHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.aHash(cv2.imread(img2))
            n = cls.cmpHash(hash1, hash2)
            logger.info(f'均值哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比均值哈希错误:{e}')

    @classmethod
    def dHash(cls, img1: str, img2: str) -> int:
        """
        差值哈希算法对比
        :param img1: 图片1
        :param img2: 图片2
        :return:
        """
        try:
            hash1 = AlgorithmClassify.dHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.dHash(cv2.imread(img2))
            n = cls.cmpHash(hash1, hash2)
            logger.info(f'差值哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比差值哈希错误:{e}')

    @classmethod
    def pHash(cls, img1: str, img2: str) -> int:
        """
        差值哈希算法对比
        :param img1: 图片1
        :param img2: 图片2
        :return:
        """
        try:
            hash1 = AlgorithmClassify.pHash(cv2.imread(img1))
            hash2 = AlgorithmClassify.pHash(cv2.imread(img2))
            n = cls.cmpHash(str(hash1), str(hash2))
            logger.info(f'感知哈希算法相似度:{n}')
            return n
        except Exception as e:
            logger.error(f'对比差感知哈希错误:{e}')


# Hash值对比
# Diff.aHash('/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/3.png',
#            '/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/5.png')
# Diff.dHash('/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/3.png',
#            '/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/5.png')
# Diff.pHash('/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/3.png',
#            '/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/5.png')
# Diff.classify_hist_with_split('/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/3.png',
#                               '/Users/reda-flight/Desktop/svn/reda-ui-auto/output/report_screen/1.png')
