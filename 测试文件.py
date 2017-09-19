#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/8

import datetime,time
d1 = datetime.datetime(2017,9,8)
d2 = datetime.datetime(2017,12,5)
print(time.strftime('%Y-%m-%d',time.localtime(time.time())))
print((d1 - d2).days)
print(datetime.datetime.now())
