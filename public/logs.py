# -*- coding: utf-8 -*-
# @File: logs.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2020/10/22  11:31

import os
import time
from loguru import logger
from config.setting import LOG_DIR


class SetLog:
    """
    日志设置类  使用 logger 请从此logs目录导入
    """

    DAY = time.strftime("%Y-%m-%d", time.localtime(time.time()))

    LOG_PATH = os.path.join(LOG_DIR, f'{DAY}_all.log')

    ERR_LOG_PATH = os.path.join(LOG_DIR, f'{DAY}_err.log')

    logger.add(LOG_PATH, rotation="00:00", encoding='utf-8' )

    logger.add(ERR_LOG_PATH, rotation="00:00", encoding='utf-8', level='ERROR', )
