from xadmin.plugins.actions import BaseActionView
from xadmin.views.base import filter_hook
from django.core.exceptions import PermissionDenied
from xadmin.util import model_ngettext
from django.utils.encoding import force_text
from django.db import router
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.contrib.admin.utils import get_deleted_objects
from function_settings.models import Function_setup
from talk.models import Talk_manage


class MyUpdateAction(BaseActionView):
    # 这个是执行函数名
    action_name = "update_function"
    # 这个是显示的名字
    description = "批量设置功能"

    # 这里是是否启用自定义模板
    delete_confirmation_template = None
    delete_selected_confirmation_template = None

    delete_models_batch = True

    model_perm = 'change'
    # icon = 'fa fa-times'

    @filter_hook
    def do_action(self, queryset):  #点击批量修改标签后执行的操作
        if not self.has_change_permission(): #获取权限
            raise PermissionDenied
        # Check that the user has change permission for the actual model
        function_list=Function_setup.objects.all()
        context = self.get_context()
        context['list']=function_list
        context['queryset']=[i.id for i in queryset]



        return TemplateResponse(self.request, self.delete_selected_confirmation_template or
                                self.get_template_list('views/change_function.html'), context)

# class TalkUpdateAction(BaseActionView):   批量添加话术
#     # 这个是执行函数名
#     action_name = "update_talk"
#     # 这个是显示的名字
#     description = "批量添加话术"
#
#     # 这里是是否启用自定义模板
#     delete_confirmation_template = None
#     delete_selected_confirmation_template = None
#
#     delete_models_batch = True
#
#     model_perm = 'change'
#     # icon = 'fa fa-times'
#
#     @filter_hook
#     def do_action(self, queryset):  #点击批量修改标签后执行的操作
#         if not self.has_change_permission(): #获取权限
#             raise PermissionDenied
#         # Check that the user has change permission for the actual model
#         if self.request.user.is_superuser:
#             talk_list=Talk_manage.objects.all()
#         else:
#             talk_list = Talk_manage.objects.filter(user=self.request.user)
#         context = self.get_context()
#         context['list']=talk_list
#         context['queryset']=[i.id for i in queryset]
#
#
#
#         return TemplateResponse(self.request, self.delete_selected_confirmation_template or
#                                 self.get_template_list('views/change_talk.html'), context)
