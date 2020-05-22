# Generated by Django 2.2.3 on 2019-12-28 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system_setup', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='user_link_setup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_setup', to=settings.AUTH_USER_MODEL, verbose_name='用户信息'),
        ),
        migrations.AlterUniqueTogether(
            name='user_link_setup',
            unique_together={('user', 'set_up')},
        ),
    ]
