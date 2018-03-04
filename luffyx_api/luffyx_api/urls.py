"""luffyx_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
from app import shopping_car
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view()),
    url(r'^courses/$', views.CourseView.as_view()),
    url(r'^courses/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', views.CourseView.as_view()),
    url(r'^degreecourse/$', views.DegreeCourseView.as_view()),
    url(r'^degreecourse/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', views.DegreeCourseView.as_view()),
    url(r'^news/$', views.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', views.NewsView.as_view()),


    url(r'^shopping_car/$', shopping_car.ShoppingView.as_view()),

    url(r'^settlement/$', shopping_car.SettlementView.as_view()),
    url(r'^couponprice/$', shopping_car.CouPonPriceView.as_view()),

    url(r'^shopping/$', views.ShoppingCarView.as_view()),

]
