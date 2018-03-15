from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
import json
from app.utils.auth.api_view import AuthAPIView
from app.utils.exception import PricePolicyDoesNotExist
from django.conf import settings
from pool import POOL
from app import models

import redis
CONN = redis.Redis(connection_pool=POOL)


class LoginView(APIView):
    authentication_classes=[]
    def get(self,request,*args,**kwargs):
        self.dispatch()
        ret = {
            'code':1000,
            'data':'老男孩'
        }
        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

    def post(self,request,*args,**kwargs):
        ret = {
            'code': 1000,
            'username': '',
            'token': ''

        }

        body = request.body
        read_body = json.loads(body)

        user_obj = models.Account.objects.filter(**read_body).first()

        if user_obj:
            #print(user_obj)
            ret['username'] = user_obj.username

            ret['token'] = user_obj.userauthtoken.token
        else:
            #ret['code'] = 404

            return HttpResponse('没有该用户，无法登陆')

        response = JsonResponse(ret)
        response['Access-Control-Allow-Origin'] = '*'
        return response


    def options(self,request,*args,**kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        # response['Access-Control-Allow-Methods'] = 'PUT'
        return response

class CourseSerializer(serializers.ModelSerializer):
    price=serializers.SerializerMethodField()
    prices=serializers.SerializerMethodField()
    class Meta:
        model = models.Course
        fields = "__all__"
        depth = 1
    def get_price(self,obj):
        ret=[]
        for i in models.PricePolicy.objects.all():
            if i.content_object==obj:
                ret.append(i.price)

        return min(ret)

    def get_prices(self,obj):
        ret=[]
        for i in models.PricePolicy.objects.all():
            if i.content_object==obj:
                ret.append({'price':i.price,'valid_period':i.get_valid_period_display()})
        return ret

class CourseDetiailSerializer(serializers.ModelSerializer):
    oftenaskedquestion=serializers.SerializerMethodField()
    recommend=serializers.SerializerMethodField()
    class Meta:
        model = models.CourseDetail
        fields = "__all__"
        depth = 1

    def get_oftenaskedquestion(self, obj):

        ret = []
        for i in models.OftenAskedQuestion.objects.all():
            if i.content_object==obj.course:
                ret.append({'question':i.question,'answer':i.answer})
        return ret
    def get_recommend(self,obj):
        ret=[]
        for i in obj.recommend_courses.all():
            ret.append({'id':i.id,'name':i.name})

        return ret

class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections=serializers.SerializerMethodField()
    class Meta:
        model = models.CourseChapter
        fields = "__all__"
        depth = 1

    def get_coursesections(self,obj):
        ret=[]
        for i in obj.coursesections.all():
            ret.append({'name':i.name,'video_time':i.video_time})
        return ret

class CourseView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            courses = models.CourseDetail.objects.get(course_id=pk)
            courses_obj = CourseDetiailSerializer(instance=courses)

            coursechapterList=models.CourseChapter.objects.filter(course_id=pk)
            coursechapter_obj=CourseChapterSerializer(instance=coursechapterList,many=True)

            course=models.Course.objects.get(id=pk)
            course.level=course.get_level_display()
            course_obj=CourseSerializer(instance=course)
            ret = {
                'code': "1000",
                'courses': courses_obj.data,
                'course': course_obj.data,
                'coursechapterList':coursechapter_obj.data

            }
        else:
            course_list = models.Course.objects.all()
            for i in course_list:
                i.level = i.get_level_display()
            obj = CourseSerializer(instance=course_list, many=True)
            ret = {
                'code': 1000,
                'courseList': obj.data,

            }
        response = Response(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

class DegreeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = "__all__"
        depth = 1

class DegreeCourseView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            degreecourse = models.DegreeCourse.objects.get(id=pk)
            degreecourse_obj = DegreeCourseSerializer(instance=degreecourse)

            courseList=models.Course.objects.filter(degree_course_id=pk)
            for i in courseList:
                i.level = i.get_level_display()
            course=CourseSerializer(instance=courseList,many=True)
            ret = {
                'code': "1000",
                'degreecourse': degreecourse_obj.data,
                'courseList':course.data
            }
        else:
            degreecourse_list = models.DegreeCourse.objects.all()
            obj = DegreeCourseSerializer(instance=degreecourse_list, many=True)
            ret = {
                'code': 1000,
                'degreecourseList': obj.data,
            }
        response = Response(ret)
        response['Access-Control-Allow-Origin'] = "*"
        return response

class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
        depth = 2

class NewsView(APIView):
    """
    深科技页面
    """

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk:
            article = models.Article.objects.filter(pk=pk).first()
            ser = NewsSerializers(instance=article,many=False)
            response = JsonResponse(ser.data,safe=False)
        else:
            article_list = models.Article.objects.all()
            ser = NewsSerializers(instance=article_list, many=True)
            # print(ser.data)
            response = JsonResponse(ser.data, safe=False)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
        return response

    def put(self,request,*args,**kwargs):
        article_id = request.GET.get('article_id')
        agree_num = request.GET.get('agree_num')
        agree_info = request.GET.get('agree_info')

        article_col_id = request.GET.get('article_id')
        collect_num = request.GET.get('collect_num')
        collect_msg = request.GET.get('collect_msg')
        collect = request.GET.get('collect')
        if collect_msg:
            # 证明是收藏
            user = models.Account.objects.filter(pk=1).first()
            collect_msg = models.Article.objects.filter(pk=article_col_id).update(collect_num=collect_num)
            models.Collection.objects.create(account=user)
            if collect_msg:
                if collect:
                    ret = {"msg":"收藏成功"}
                    response = JsonResponse(ret)
                else:
                    ret = {"msg":"取消收藏成功"}
                    response = JsonResponse(ret)
            else:
                ret = {"msg":"收藏失败"}
                response = JsonResponse(ret)
            response['Access-Control-Allow-Origin']= '*'
            response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
            return response

        else:
            agree_msg = models.Article.objects.filter(pk=article_id).update(agree_num=agree_num)
            if agree_msg:
                if agree_info:
                    ret = {"msg":"点赞成功"}
                    response=JsonResponse(ret)

                else:
                    ret = {"msg":"取消点赞成功"}
                    response = JsonResponse(ret)
            else:
                ret = {"msg":"点赞失败"}
                response = JsonResponse(ret)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
            return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        response['Access-Control-Allow-Methods'] = '*'
        return response

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'
        depth = 1

class CommentView(APIView):

    def get(self, request, *args, **kwargs):
        comment_list = models.Comment.objects.all()
        ser = CommentSerializers(instance=comment_list, many=True)
        response = JsonResponse(ser.data,safe=False)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
        return response

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'  # 允许的请求头
        response['Access-Control-Allow-Methods'] = '*'
        # return response
        return response


class ShoppingCarView(AuthAPIView,APIView):

    def get(self,request,*args,**kwargs):
        """
        查看购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        course = CONN.hget(settings.LUFFY_SHOPPING_CAR,request.user.id)
        ret = json.loads(course.decode('utf-8'))
        return Response(ret)

    def post(self,request,*args,**kwargs):
        """
        获取课程ID和价格策略ID，放入redis
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {'code':1000,'msg':None}
        try:
            course_id = request.data.get('course_id')
            price_policy_id = request.data.get('price_policy_id')
            # 1. 获取课程
            course_obj = models.Course.objects.get(id=course_id)
            # 2. 获取当前课程的所有价格策略: id, 有效期，价格
            price_policy_list = []
            flag = False
            price_policy_objs = course_obj.price_policy.all()
            for item in price_policy_objs:
                if item.id == price_policy_id:
                    flag = True
                price_policy_list.append({'id':item.id, 'valid_period':item.get_valid_period_display(),'price':item.price})
            if not flag:
                raise PricePolicyDoesNotExist()

            # 3. 课程和价格策略均没有问题，将课程和价格策略放到redis中
            # 课程id,课程图片地址,课程标题，所有价格策略，默认价格策略
            course_dict = {
                'id': course_obj.id,
                'img': course_obj.course_img,
                'title': course_obj.name,
                'price_policy_list': price_policy_list,
                'default_policy_id': price_policy_id
            }

            # a. 获取当前用户购物车中的课程 car = {1: {,,,}, 2:{....}}
            # b. car[course_obj.id] = course_dict
            # c. conn.hset('luffy_shopping_car',request.user.id,car)
            nothing = CONN.hget(settings.LUFFY_SHOPPING_CAR, request.user.id)
            if not nothing:
                data = {course_obj.id: course_dict}
            else:
                data = json.loads(nothing.decode('utf-8'))
                data[course_obj.id] = course_dict

            CONN.hset(settings.LUFFY_SHOPPING_CAR, request.user.id, json.dumps(data))

        except ObjectDoesNotExist as e:
            ret['code'] = 1001
            ret['msg'] = "课程不存在"
        except PricePolicyDoesNotExist as e:
            ret['code'] = 1002
            ret['msg'] = "价格策略不存在"
        except Exception as e:
            ret['code'] = 1003
            ret['msg'] = "添加购物车异常"

        return Response(ret)




