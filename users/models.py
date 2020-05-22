from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import random, time
from django.utils.safestring import mark_safe
from function_settings.models import Function_setup
from talk.models import Talk_manage, Weibo_manage


def generate_random_str(randomlength=16):  # 生成随机字符串
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


# Create your models here.

class User(AbstractUser):
    account_num = models.CharField(default=0, verbose_name='分配的账号个数', max_length=30)
    phone = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True)
    remaining_accounts = models.IntegerField(verbose_name='剩余的账号数量', null=True, blank=True)
    increase_time = models.IntegerField(verbose_name='添加时间', null=True, help_text='单位是：天', default=0)
    over_time = models.IntegerField(verbose_name='过期时间', null=True, blank=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_over_date(self):
        if time.time() >= self.over_time:
            return mark_safe(
                '<p style="color:red" >{0} 已过期<p/>'.format(
                    time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(self.over_time)))
            )
        else:
            return mark_safe(
                '<p>{0}<p/>'.format(
                    time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(self.over_time)))
            )


    get_over_date.short_description = '过期时间'

class Account_manage(models.Model):
    Status = (
        ('1', '开启'),
        ('0', '关闭')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户信息', related_name='account')
    account_name = models.CharField(max_length=30, verbose_name='账号用户名', blank=True, unique=True,
                                    default=generate_random_str, help_text='创建账号时会自动生成账号及密码！')
    password = models.CharField(max_length=30, verbose_name='账号密码', blank=True, default=generate_random_str)
    operation_type=models.IntegerField(verbose_name='操作类型',null=True,help_text='0:养号,1:大V养号,2:大v粉丝发私信,3:同城私信')
    big_v = models.CharField(max_length=50, verbose_name='大V账号', null=True)
    status = models.CharField(choices=Status, default='1', verbose_name='状态', max_length=2)
    equipment_id = models.CharField(max_length=40, verbose_name='设备ID', null=True, blank=True)
    function_setup = models.ForeignKey(Function_setup, verbose_name='功能设置', blank=True, null=True,
                                       related_name='account_manage', on_delete=models.SET_NULL)
    # talk = models.ManyToManyField(Talk_manage, verbose_name='话术设置', blank=True, related_name='account_manage')
    # weibo_manage = models.ManyToManyField(Weibo_manage, verbose_name='微博设置', blank=True, related_name='account_manage')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '账号管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.account_name
