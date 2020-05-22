from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
import os
from django.dispatch import Signal
from django.db.models.signals import post_save, post_delete, pre_save
from .models import Douyin_setup, User_link_setup
from users.models import User


# 调用signal方法

@receiver(post_save, sender=Douyin_setup)  # 当模型调用save方法时，发送信息，调用signal_work函数
def signal_work(sender, instance, created, **kwargs):  # 信号的接受者
    if created:
        try:
            user_list = User.objects.filter(is_superuser=False)
            add_list = []
            for user in user_list:
                user_and_setup = User_link_setup(user=user, set_up=instance, setup_value=instance.default_value)
                add_list.append(user_and_setup)
            User_link_setup.objects.bulk_create(add_list)
        except:  # 发生错误时，删除新建的设置
            douyin_setup = Douyin_setup.objects.get(id=instance.id)
            douyin_setup.delete()
    else:
        try:
            User_link_setup.objects.filter(set_up=instance).update(setup_value=instance.default_value)
        except:
            raise ValueError('保存出错，请重新保存')
