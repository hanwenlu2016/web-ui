# -*- coding: utf-8 -*-
# @File: jd.py
# @Author: HanWenLu
# @E-mail: wenlupay@163.com
# @Time: 2021/1/14  16:02

import time

from public.getcasedata import GetCaseData
from public.app.appbase import AppBase



class Jd(AppBase):
    """
    京东demo
    """

    def openjd(self):
        jd = GetCaseData('jd.yaml', 'openjd')

        time.sleep(2)
        self.used_click(types=jd.types(0), locate=jd.locate(0))

        relust = self.used_text(types=jd.types(1), locate=jd.locate(1))
        time.sleep(1)

        assert relust == jd.expect(1)
