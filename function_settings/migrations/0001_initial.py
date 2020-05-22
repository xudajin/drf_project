# Generated by Django 2.2.3 on 2019-12-28 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Function_setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True, verbose_name='功能名称')),
                ('key', models.CharField(max_length=30, null=True, verbose_name='操作key')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '功能设置',
                'verbose_name_plural': '功能设置',
            },
        ),
    ]
