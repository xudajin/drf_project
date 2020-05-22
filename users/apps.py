from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name='用户系统'

    def ready(self):
        import users.my_signal  #加载signal
