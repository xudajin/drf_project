from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import reverse, redirect
from rest_framework.views import APIView
from .models import Account_manage
import time, jwt, json
from function_settings.models import Function_setup
from talk.models import Talk_manage, Weibo_manage, Retransmission, Commentary
from system_setup.models import User_link_setup, Culture_account
from rest_framework.viewsets import GenericViewSet
from .serializers import Talk_manageSerializers, Weibo_manageSerializers, Function_setupSerializers, \
    Account_loginSerializers, Set_upSerializers, RetransmissionSerializers, CommentarySerializers
from rest_framework.response import Response
from utils.own_setting import APIResponse, AccountAuthentication

from rest_framework_jwt.serializers import jwt_encode_handler
from yunkong.settings import SECRET_KEY
from system_setup.serializers import Culture_accountSerializer

# 批量添加功能
def set_function(request):
    if request.method == 'POST':
        account_list = request.POST.getlist('userid', None)
        function = Function_setup.objects.filter(id__in=request.POST.getlist('function', None))
        for i in account_list:
            account = Account_manage.objects.get(id=int(i))
            account.function_setup.add(*function)
    return redirect(r'/xadmin/users/account_manage/')


# 批量添加话术
def set_talk(request):
    if request.method == 'POST':
        account_list = request.POST.getlist('userid', None)
        talk = Talk_manage.objects.filter(id__in=request.POST.getlist('talk', None))
        for i in account_list:
            account = Account_manage.objects.get(id=int(i))
            account.talk.add(*talk)
    return redirect(r'/xadmin/users/account_manage/')


class Get_info(GenericViewSet):
    authentication_classes = [AccountAuthentication]

    def list(self, request):
        return APIResponse(200, 'success', 'data')


class Accountlogin(APIView):
    serializer_class = Account_loginSerializers
    permission_classes = []

    def post(self, request):
        serializer = Account_loginSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account = Account_manage.objects.get(account_name=serializer.data['account_name'])
            account.equipment_id = serializer.data['equipment_id']
            account.save()
            talk = Talk_manage.objects.filter(
                account=account)[0:3]
            talk = Talk_manageSerializers(talk, many=True)
            weibo = Weibo_manage.objects.filter(
                account=account)
            weibo = Weibo_manageSerializers(weibo, many=True)
            function_set = Function_setup.objects.filter(account_manage=account)
            function_set = Function_setupSerializers(function_set, many=True)
            set_up = Set_upSerializers(User_link_setup.objects.all(), many=True)
            retransmission = RetransmissionSerializers(Retransmission.objects.filter(account=account), many=True)
            commentary = CommentarySerializers(Commentary.objects.filter(account=account), many=True)
            cultrue_account = Culture_accountSerializer(Culture_account.objects.filter(user=account.user),many=True)
            if cultrue_account:
                cultrue_account=cultrue_account.data[0]
            # 设置格式
            set_dict = {}  # 抖音app设置的信息字典
            for i in set_up.data:
                set_dict[i['set_up']['key']] = i['setup_value']

            set = {
                'exp': int(time.time() + 60 * 60 * 24),  # 超时时间
                'iat': int(time.time()),  # 生成TOKEN时间
                'account': serializer.validated_data['account_name']
            }
            token = jwt.encode(set, SECRET_KEY, algorithm='HS256')
            data = {
                'token': token,
                'id': account.id,    
                'operation_type': account.operation_type,
                'big_v': account.big_v,     #微
                'weibo': [(i['weibo_account'], i['weibo_password']) for i in weibo.data],
                'function_set': function_set.data,
                'talk': [(i['talk_content']) for i in talk.data],
                'set_up': set_dict,
                'retransmission': retransmission.data,
                'commentary': commentary.data,
                'culture_account': cultrue_account,
            }
            return APIResponse(200, 'success', data)


class Weiboinfo(APIView):
    authentication_classes = [AccountAuthentication]

    def post(self,request):
        print(request.user)
        weibo = Weibo_manage.objects.filter(
            account=request.user)
        weibo = Weibo_manageSerializers(weibo, many=True)
        talk = Talk_manage.objects.filter(
                account=request.user)[0:3]
        talk = Talk_manageSerializers(talk, many=True)

        data={
        'weibo': [(i['weibo_account'], i['weibo_password'],i['big_v']) for i in weibo.data],
        'talk' : [i['talk_content'] for i in talk.data]
        }
        return APIResponse(200, 'success', data)