#! /usr/bin/env python
# -*- coding: utf-8 -*-
#  Author :    张宁阳
#  date：      2018/3/2
from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse

from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from app import models
from app.redis_pool import conn
import json
from django.conf import settings
from app.auth import AuthAPIView
class PricePolicyDoesNotExist(Exception):
    """The requested object does not exist"""
    pass
class courseDosenotExist(Exception):
    pass
class ShoppingView(AuthAPIView,APIView):
    def get(self,request,*args,**kwargs):
        """返回当前用户的所有价格策略"""
        course = conn.hget(settings.SHOPPING_CAR, request.user.id)
        course_dict = json.loads(course.decode('utf-8'))
        return Response(course_dict)
    def post(self,request,*args,**kwargs):
        """ 获取课程ID和价格策略ID，放入redis"""
        ret = {'code': 1000, 'msg': None}
        try:
            course_id = request.data.get('course_id')
            price_policy_id = request.data.get('price_policy_id')
            course_obj = models.Course.objects.get(id=course_id)
            course_obj_pric_policy=course_obj.price_policy.all()
            #id, 有效期，价格
            price_policy_list=[]
            flag = False
            for i in course_obj_pric_policy:
                if i.id==price_policy_id:
                    flag = True
                price_policy_list.append({"id":i.id,"valid_period":i.get_valid_period_display(),"price":i.price})
            if not flag:
                raise PricePolicyDoesNotExist()
            #放入redis
            # 课程id,课程图片地址,课程标题，所有价格策略，默认价格策略
            course_dict = {
                'id': course_obj.id,
                'img': course_obj.course_img,
                'title': course_obj.name,
                'price_policy_list': price_policy_list,
                'default_policy_id': price_policy_id
            }
            # {"user.id":{"course_id":course_dict}}
            nothing = conn.hget(settings.SHOPPING_CAR, request.user.id)
            if not nothing:
                data = {course_obj.id: course_dict}
            else:
                data = json.loads(nothing.decode('utf-8'))
                data[course_obj.id] = course_dict
                ret['msg'] = course_dict
            conn.hset(settings.SHOPPING_CAR, request.user.id, json.dumps(data))
        except ObjectDoesNotExist as e:
            ret["code"]=1001
            ret["msg"]="课程不存在"
        except PricePolicyDoesNotExist as e:
            ret['code'] = 1002
            ret['msg'] = "价格策略不存在"
        except Exception as e:
            ret['code'] = 1003
            ret['msg'] = "添加购物车异常"
        return Response(ret)
    def patch(self,request,*args,**kwargs):
        """ 获取课程ID和价格策略ID，更新redis"""
        ret = {'code': 1000, 'msg': None}
        try:
            course_id = request.data.get('course_id')
            price_policy_id = request.data.get('price_policy_id')

            """返回当前用户的所有价格策略"""
            course = conn.hget(settings.SHOPPING_CAR, request.user.id)
            course_dict = json.loads(course.decode('utf-8'))
            ks=[]
            for k, v in course_dict.items():
                ks.append(k)

            for k,v in course_dict.items():
                if str(course_id) not in ks:raise courseDosenotExist
                if str(course_id) == k:
                    price_list=[p["id"] for p in v["price_policy_list"]]
                    if price_policy_id not in price_list:raise PricePolicyDoesNotExist
                    course_dict[str(course_id)]["default_policy_id"]=price_policy_id
            ret['msg'] = course_dict
            conn.hset(settings.SHOPPING_CAR, request.user.id, json.dumps(course_dict))
        except courseDosenotExist as e:
            ret['code'] = 1001
            ret['msg'] = "课程不存在"
        except PricePolicyDoesNotExist as e:
            ret['code'] = 1002
            ret['msg'] = "价格不存在"
        # except Exception as e:
        #     ret['code'] = 1003
        #     ret['msg'] = "更新购物车异常"
        return Response(ret)
    def delete(self,request,*args,**kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            course_id = request.data.get('course_id')
            course = conn.hget(settings.SHOPPING_CAR, request.user.id)
            course_dict = json.loads(course.decode('utf-8'))
            ks = []
            for k, v in course_dict.items():
                ks.append(k)
            if str(course_id) not in ks:
                raise courseDosenotExist
            else:
                del course_dict[str(course_id)]
                conn.hset(settings.SHOPPING_CAR, request.user.id, json.dumps(course_dict))
        except courseDosenotExist as e:
            ret['code'] = 1001
            ret['msg'] = "课程不存在"
        return Response(ret)