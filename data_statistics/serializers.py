from rest_framework import serializers
from users.models import Account_manage
from function_settings.models import Function_setup


class Data_countSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(required=True)
    function_type = serializers.IntegerField(required=True)

    # def validate_account_id(self, account_id):
    #     account = Account_manage.objects.filter(id=account_id)
    #     if not account:
    #         raise serializers.ValidationError('账号id错误')
    #     return account_id

    # def validate_function_type(self, function_type):
    #     function = Function_setup.objects.filter(id=function_type)
    #     if not function:
    #         raise serializers.ValidationError('功能类型错误')
    #     return function_type

