from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from utils.own_setting import APIResponse, AccountAuthentication
from .serializers import Data_countSerializer
from .models import Data_statistics
import time, datetime
from django.core.cache import cache   # django 缓存



class Count(APIView):
    # authentication_classes = [AccountAuthentication,]
    def post(self, request):
        serializers = Data_countSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            day_time = int(time.mktime(datetime.date.today().timetuple()))  # 当天零时的时间戳
            account_id = serializers.data['account_id']  # 账号id
            function_type = serializers.data['function_type']  # 功能id
            # 操作redis
            value = cache.get('_{0},{1},{2}'.format(account_id, function_type, day_time))  # 获取redis中的键名
            if value:  # 判断键名存不存在，若键名存在，表示账号，用户，日期 全部相等
                value[2] += 1  # 将值取出并加1
                cache.set('_{0},{1},{2}'.format(account_id, function_type, day_time), value,timeout=3600*24)
                print(111, cache.get('_{0},{1},{2}'.format(account_id, function_type, day_time)))
            else:
                cache.set('_{0},{1},{2}'.format(account_id, function_type, day_time),
                          [account_id, function_type, 1, day_time],timeout=3600*24)
                print(cache.get('_{0},{1},{2}'.format(account_id, function_type, day_time)))
            return APIResponse(200, 'success')



import redis
from users.models import User
from django.db import transaction
class Redis_to_sql(APIView):
    # authentication_classes = [AccountAuthentication, ]
    def post(self, request):
        name=request.data.get('name',None)
        if not name or not User.objects.filter(username=name).exists(): #判断用户是否存在
            return APIResponse(404, 'error')

        with transaction.atomic():   #使用事务
            save_id = transaction.savepoint()   #创建 事务保存点
            keys = cache.keys("_*,*")  # cache.keys("*") 用 "*"  表示所有keys
            count_list = []
            try:
                for key in keys:  # 遍历键取值
                    value = cache.get(key)  #获取值
                    Data_statistics.objects.update_or_create(account_id=value[0], function_type=value[1],write_time=value[3], defaults={"total_number":value[2]})
                return APIResponse(200,'success')
            except:
                transaction.savepoint_rollback(save_id)
                return APIResponse(404,'error')
