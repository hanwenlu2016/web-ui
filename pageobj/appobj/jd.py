# -*- coding: utf-8 -*-
# @File: jd.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  16:02

import time

from public.getcasedata import GetCaseData
from public.app.appbase import Base
from public.logs import logger


class Jd(Base):
    """
    京东demo
    """

    def openjd(self):
        jd = GetCaseData('jd.yaml', 'openjd')

        time.sleep(2)
        self.swipe_down(1)

        time.sleep(2)
        # self.clicks(jd.types(0), jd.locate(0))
        #
        # time.sleep(2)
        # relust = self.get_text(jd.types(1), jd.locate(1))
        # time.sleep(2)

        # assert relust == jd.expect(1)
