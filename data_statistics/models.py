from django.db import models
from django.utils import timezone
import time, datetime

# Create your models here.
day_time = int(time.mktime(datetime.date.today().timetuple()))  # 获取当天 0时的时间戳


class Data_statistics(models.Model):
    account_id = models.IntegerField(verbose_name='账号id')
    function_type = models.IntegerField(verbose_name='功能类型')
    total_number = models.IntegerField(verbose_name='使用次数', default=1)
    write_time = models.IntegerField(verbose_name='数据写入日期', default=day_time)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '数据统计'
        verbose_name_plural = verbose_name

    def write_day(self):
        return datetime.datetime.fromtimestamp(self.write_time).strftime("%Y--%m--%d")
    write_day.short_description='请求日期'



    def __str__(self):
        return '账号{}的统计数据'.format(self.account_id)
