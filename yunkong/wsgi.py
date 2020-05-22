"""
WSGI config for yunkong project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os,sys

sys.path.append(r'C:\Users\Administrator\Envs\yunkong\Lib\site-packages')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yunkong.settings')

application = get_wsgi_application()
