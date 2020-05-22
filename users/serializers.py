from rest_framework import serializers

from talk.models import Talk_manage, Weibo_manage, Commentary, Retransmission
from function_settings.models import Function_setup
from system_setup.models import User_link_setup, Douyin_setup
from .models import Account_manage
from utils.own_setting import APIResponse
from rest_framework_jwt.serializers import jwt_encode_handler


class Account_loginSerializers(serializers.Serializer):
    account_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    equipment_id = serializers.CharField(required=True)

    def validate(self, attrs):
        account = Account_manage.objects.filter(account_name=attrs['account_name'])
        if account:
            if account[0].password != attrs['password']:
                raise serializers.ValidationError('账号或密码错误')

            if account[0].equipment_id:
                if attrs['equipment_id'] != account[0].equipment_id:
                    raise serializers.ValidationError('设备ID错误')

            return attrs

        else:
            raise serializers.ValidationError('账号或者密码错误')


class Talk_manageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Talk_manage
        fields = ('talk_content',)


class Weibo_manageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Weibo_manage
        fields = ('id', 'weibo_account', 'weibo_password','big_v')


class Function_setupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Function_setup
        fields = ('title', 'key')


class Douyin_setupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Douyin_setup
        fields = ('key',)


class Set_upSerializers(serializers.ModelSerializer):
    set_up = Douyin_setupSerializers()

    class Meta:
        model = User_link_setup
        fields = ('set_up', 'setup_value')


class RetransmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Retransmission
        fields = ('forward_content',)


class CommentarySerializers(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        exclude = ('id', 'user', 'account', 'date_joined')
