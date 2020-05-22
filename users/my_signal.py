from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Account_manage
import os, time, datetime
from django.dispatch import Signal
from django.db.models.signals import post_save, post_delete, pre_save
from .models import User, Account_manage
from system_setup.models import Douyin_setup, User_link_setup,Culture_account


# 调用signal方法

@receiver(post_delete, sender=Account_manage)  # 当模型调用delete方法时，发送信息，调用signal_work函数
def signal_work(sender, instance, **kwargs):  # 信号的接受者
    account_num = instance.user.account_num
    user = User.objects.get(username=instance.user)
    # 重新统计剩余的账号数量
    user.remaining_accounts = int(account_num) - len(Account_manage.objects.filter(user=instance.user))
    user.save()


@receiver(post_save, sender=Account_manage)
def savework(sender, instance, created, **kwargs):
    if created:
        account_num = instance.user.account_num
        user = User.objects.get(username=instance.user)
        # 重新统计剩余的账号数量
        user.remaining_accounts = int(account_num) - len(Account_manage.objects.filter(user=instance.user))
        user.save()


# 当创建用户时自动添加抖音APP配置,养号功能到子用户
@receiver(post_save, sender=User)
def setup_to_user(sender, instance, created, using, **kwargs):  # created 判断是否创建新的数据
    try:
        if created:
            set_list = Douyin_setup.objects.all()
            add_list = []
            for set in set_list:
                user_and_setup = User_link_setup(user=instance, set_up=set, setup_value=set.default_value)
                add_list.append(user_and_setup)
            User_link_setup.objects.bulk_create(add_list)  # bulk_create是批量创建
            culture_account = Culture_account.objects.create(user=instance)  # 自动创建养号设置
            culture_account.save()
    except:
        user = User.objects.get(id=instance.id)
        user.delete()
