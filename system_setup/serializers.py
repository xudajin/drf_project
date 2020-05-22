from rest_framework import serializers
from .models import Culture_account
from utils.own_setting import APIResponse


class Culture_accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture_account
        exclude=('date_joined','user','id')



