from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Douyin_setup(models.Model):  # 抖音设置
    title = models.CharField(max_length=30, verbose_name='标题', null=True)
    key = models.CharField(max_length=30, verbose_name='操作key', null=True)
    default_value = models.CharField(max_length=30, verbose_name='设置默认值', default='0')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '全局抖音APP设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class User_link_setup(models.Model):  # 用户——抖音设置关系
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_setup', verbose_name='用户信息')
    set_up = models.ForeignKey(Douyin_setup, on_delete=models.CASCADE, related_name='link_user', verbose_name='设置信息')
    setup_value = models.IntegerField(verbose_name='数值', null=True,help_text='时间的单位为：毫秒')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        unique_together = ('user', 'set_up',)
        verbose_name = '个人抖音app设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}的设置{1}'.format(self.user, self.set_up)

    def get_key_name(self):
        return self.set_up.key

    get_key_name.short_description = 'key值'


class Backend_setup(models.Model):  # 后台系统设置
    title = models.CharField(max_length=30, verbose_name='标题', null=True)
    key_word = models.CharField(max_length=30, verbose_name='操作key', null=True)
    value = models.CharField(max_length=30, verbose_name='设置参数', null=True)
    STATUS = (
        ('1', '开启'),
        ('0', '关闭'),
    )
    status = models.CharField(choices=STATUS, max_length=2, verbose_name='状态', default='1')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '后台系统设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


#养号功能
class Culture_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='culture_account', verbose_name='养号设置')
    limit_watch = models.IntegerField(verbose_name='每日观看上限', help_text='单位：次数', default=50)
    watch_duration_min = models.IntegerField(verbose_name='观看时长最小值', help_text='单位：毫秒', default=3000)
    watch_duration_max = models.IntegerField(verbose_name='观看时长最大值', default=7000,help_text='单位：毫秒')
    watch_times = models.IntegerField(verbose_name='观看视频数', help_text='观看多少个视频后，随机暂停', default=3)
    pause_time_min = models.IntegerField(verbose_name='暂停时间最小值', help_text='单位：毫秒', default=3000)
    pause_time_max = models.IntegerField(verbose_name='暂停时间最大值', default=6000,help_text='单位：毫秒')
    nice_probability = models.FloatField(verbose_name='点赞概率', help_text='请填写0到1之间的小数', default=0.2)
    comment_probability = models.FloatField(verbose_name='评论概率', default=0.2)
    comment_nice_probability = models.FloatField(verbose_name='在评论区点赞的概率', default=0.2, help_text='请填写0到1之间的小数')
    comment_nice_min_times = models.IntegerField(verbose_name='评论区点赞的最小次数', default=1)
    comment_nice_max_times = models.IntegerField(verbose_name='评论区点赞的最大次数', default=3)
    forward_probability = models.FloatField(verbose_name='转发概率', help_text='请填写0到1之间的小数', default=0.2)
    follow_author_probability = models.FloatField(verbose_name='关注作者的概率', default=0.2, help_text='请填写0到1之间的小数')
    follow_author_pause_time_min = models.IntegerField(verbose_name='关注作者前的暂停时间最小值', help_text='单位：毫秒', default=2000)
    follow_author_pause_time_max = models.IntegerField(verbose_name='关注作者前的暂停时间最大值', default=4000,help_text='单位：毫秒')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True)

    class Meta:
        verbose_name = '养号规则设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '养号规则'

    def clean(self):  # 自定义数据验证
        plus1 = self.comment_nice_probability + self.nice_probability
        plus2 = self.comment_probability + self.forward_probability
        plus3 = plus1 + plus2
        if plus3 + self.follow_author_probability != 1:
            raise ValidationError('请确保所有概率参数总和为1！')

        if self.watch_duration_min >= self.watch_duration_max or self.pause_time_min >= self.pause_time_max or self.comment_nice_min_times >= self.comment_nice_max_times or self.follow_author_pause_time_min >= self.follow_author_pause_time_max:
            raise ValidationError('请检查最小值不能大于或等于最大值!')
        
