"""yunkong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path
from django.views.static import serve
from yunkong.settings import MEDIA_ROOT
import xadmin
from rest_framework_jwt.views import obtain_jwt_token  # jwt登录验证
from users import views
from data_statistics.views import Count, Redis_to_sql
from app_d.views import download
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 媒体服务器
    # path(r'set_function', views.set_function, name='set_function'),  # 批量添加功能请求的地址
    # path(r'set_talk', views.set_talk, name='set_talk'),  # 批量添加功能请求的地址
    # 前端接口路由
    path(r'login/', obtain_jwt_token, name='login'),
    path(r'all_info/', views.Get_info.as_view({'get': 'list'}), name='all_info'),
    path(r'account_login/', views.Accountlogin.as_view(), name='account_login'),
    path(r'weibo_info/', views.Weiboinfo.as_view(), name='weibo_info'), #微博数据
    path(r'appd/', download, name='app_index'),
    path(r'count/', Count.as_view(), name='count'),  #统计数据接口
    path(r'tosql/', Redis_to_sql.as_view(), name='tosql'), #redis baocun到数据库

]
