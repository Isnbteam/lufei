#! /usr/bin/env python
# -*- coding: utf-8 -*-
#  Author :    张宁阳
#  date：      2018/3/2  
from django_redis import get_redis_connection
conn = get_redis_connection()