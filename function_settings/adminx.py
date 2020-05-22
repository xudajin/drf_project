import xadmin
from .models import Function_setup
from users.models import Account_manage, User


class Function_setupAdmin(object):
    list_display = ['id', 'title', 'key', 'date_joined']
    ordering = ['id']
    readonly_fields = ['title', 'key']

    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


xadmin.site.register(Function_setup, Function_setupAdmin)
