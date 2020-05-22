from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data_status, msg, results=None, headers=None, status=None, **kwargs):
        '''

        :param data_status: 状态码
        :param msg: 提示信息
        :param results: 附加信息,如序列化得到的数据
        :param headers:
        :param status: HTTP状态码
        :param kwargs: 其他信息
        '''
        data = {
            'code': data_status,
            'msg': msg,
        }
        if results:
            data['data'] = results
        data.update(kwargs)
        super().__init__(data=data, headers=headers, status=status)


from rest_framework.views import exception_handler


# 自定义异常处理
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = response.status_code

    return response


class LoginResponse(Response):
    def __init__(self, data_status, msg, token=None, results=None, headers=None, status=None, **kwargs):
        '''

        :param data_status: 状态码
        :param msg: 提示信息
        :param results: 附加信息,如序列化得到的数据
        :param headers:
        :param status: HTTP状态码
        :param kwargs: 其他信息
        '''
        data = {
            'code': data_status,
            'msg': msg,
            'token': token
        }
        if results:
            data['data'] = results
        data.update(kwargs)
        super().__init__(data=data, headers=headers, status=status)


import jwt
from jwt import ExpiredSignatureError, InvalidAlgorithmError, InvalidSignatureError, DecodeError
from yunkong.settings import SECRET_KEY as key
import warnings
from datetime import datetime
from calendar import timegm
from rest_framework import authentication
from rest_framework import exceptions
from users.models import Account_manage

# 重写自定义的token验证
class AccountAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.META.get('HTTP_TOKEN')  # 获取请求头中的TOKEN
        if token:  # 判断请求头中是否有token信息
            account_info = jwt.decode(token, key, algorithms='HS256')  # 默认的解密方式
            account=Account_manage.objects.get(account_name=account_info['account'])
            return (account, None)    #返回account 由 request.user 接收 account
    #       # Token超时错误
    #         raise exceptions.AuthenticationFailed('Token已经过期,请重新登录')
    #     except InvalidAlgorithmError:  # 解密方法错误
    #         raise exceptions.AuthenticationFailed('你使用的解密方式错误')
    #     except:
    #         raise exceptions.AuthenticationFailed('Token错误')
    # else:
    #     raise exceptions.AuthenticationFailed('请提交token')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
