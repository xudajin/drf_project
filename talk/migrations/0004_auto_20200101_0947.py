# Generated by Django 2.2.3 on 2020-01-01 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0003_auto_20191231_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentary', to=settings.AUTH_USER_MODEL, verbose_name='用户信息'),
        ),
    ]
