# Generated by Django 2.2.3 on 2020-01-01 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_d', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdownload',
            name='remarks',
            field=models.TextField(blank=True, max_length=120, null=True, verbose_name='版本备注'),
        ),
    ]
