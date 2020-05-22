from django.db import models

# Create your models here.
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.

class Appdownload(models.Model):
    title = models.CharField(max_length=120, verbose_name='app标题')
    remarks = models.TextField(max_length=120, verbose_name='版本备注', blank=True, null=True)
    app_file = models.FileField(upload_to='app', verbose_name='app下载地址', blank=True)
    STATUS = (
        ('1', '开启下载'),
        ('0', '关闭下载')
    )
    download = models.CharField(max_length=2, choices=STATUS, verbose_name='是否开启下载')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'app下载'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.app_file)

    # def download_app(self):
    #     return mark_safe('<a href="/media/{}">点击下载</a>'.format(self.app_file))

    # download_app.short_description = '下载链接'


class Control_download(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    STATUS = (
        ('1', '开启下载'),
        ('0', '关闭下载')
    )
    download = models.CharField(max_length=5, choices=STATUS, verbose_name='是否开启全局下载')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '下载控制'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
