from django.db import models
from django.utils import timezone
import users


# Create your models here.

class Talk_manage(models.Model):
    STATUS = (
        ('1', '开启'),
        ('0', '关闭'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户信息', related_name='talk',
                             null=True, blank=True)
    account = models.ForeignKey('users.Account_manage', on_delete=models.CASCADE, verbose_name='账号信息',
                                related_name='talk_mange', null=True, blank=True)
    talk_content = models.CharField(max_length=255, verbose_name='话术内容',help_text='话术内容默认获取前三个')
    status = models.CharField(choices=STATUS, verbose_name='状态', max_length=2, default='1')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '聊天话术'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.talk_content


class Weibo_manage(models.Model):
    STATUS = (
        ('1', '开启'),
        ('0', '关闭'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户信息', related_name='weibo',
                             null=True, blank=True,help_text='请选择关联的帐号')
    account = models.ForeignKey('users.Account_manage', on_delete=models.CASCADE, verbose_name='账号信息', help_text='请设置关联的帐号信息',
                                related_name='weibo', null=True)
    weibo_account = models.CharField(max_length=30, verbose_name='微博账号', unique=True)
    weibo_password = models.CharField(max_length=30, verbose_name='微博密码')
    big_v=models.CharField(max_length=30, verbose_name='大vID',null=True)
    status = models.CharField(choices=STATUS, verbose_name='状态', max_length=2, default='1')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '微博管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '微博账号:{}'.format(self.weibo_account)

class Commentary(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户信息', related_name='commentary',
                             null=True, blank=True)
    account = models.OneToOneField('users.Account_manage', on_delete=models.CASCADE, verbose_name='账号信息',help_text='请设置关联的帐号信息',
                                related_name='commentary', null=True, )
    comment_content = models.CharField(max_length=255, verbose_name='评论内容')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name = '评论话术'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.comment_content



class Retransmission(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户信息', related_name='retransmission',
                             null=True, blank=True)
    account = models.ForeignKey('users.Account_manage', on_delete=models.CASCADE, verbose_name='账号信息',
                                related_name='retransmission', null=True,help_text='请设置关联的帐号信息')
    forward_content = models.CharField(max_length=255, verbose_name='转发描述内容')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '转发话术'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.forward_content
