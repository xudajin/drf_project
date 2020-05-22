from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Appdownload, Control_download
from django.http import Http404
from django.http import HttpResponse

# Create your views here.

def download(request):
    if request.method=='GET':
        control_download = Control_download.objects.all()
        if control_download:
            if control_download[0].download == '0':
                raise Http404('错误')

            app_info = Appdownload.objects.filter(download='1').order_by('-id')
            print(app_info)
        return render(request,'index.html',{'app':app_info})
