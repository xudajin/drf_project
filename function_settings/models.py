from django.db import models


# Create your models here.
class Function_setup(models.Model):  # 功能设置

    title = models.CharField(max_length=30, verbose_name='功能名称', null=True)
    key = models.CharField(max_length=30, verbose_name='操作key', null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '功能设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
