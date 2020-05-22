from django.apps import AppConfig


class SystemSetupConfig(AppConfig):
    name = 'system_setup'
    verbose_name='系统设置'

    def ready(self):
        import system_setup.my_signal
