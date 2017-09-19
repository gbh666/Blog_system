#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sam"
# Date: 2017/9/8

from django import template
import datetime

register=template.Library()

@register.filter
def garden_age(starttime):

    year=starttime.year
    mon=starttime.month
    day=starttime.day

    date = datetime.datetime.now() - datetime.datetime(year,mon,day)

    return date.days




