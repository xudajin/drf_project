from django.utils.deprecation import MiddlewareMixin
from app_d.models import Control_download, Appdownload
import re
from django.http import Http404

#动态控制app下载
class Media_Middleware(MiddlewareMixin):

    def process_request(self, request):
        if re.match('/media/app/', request.path):
            allow_downloads = Control_download.objects.all()
            if allow_downloads and allow_downloads[0].download == '0':  # 判断全局下载是否开启
                raise Http404('资源不存在')
            app_downloads = Appdownload.objects.get(app_file__contains=request.path.split('/')[-1])
            if app_downloads.download == '0':   #判断该app是否允许下载
                raise Http404('资源不允许下载')
                
    def process_response(self, request, response):
        return response
