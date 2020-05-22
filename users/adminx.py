import xadmin
from xadmin import views
from .models import User, Account_manage
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import Group  # django内置的权限分组
import random, time
from django.shortcuts import redirect
from .action import MyUpdateAction
from talk.models import Talk_manage, Weibo_manage


def generate_random_str(randomlength=16):  # 生成随机字符串
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


# 全局设置
class BaseSetting(object):
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True  # 支持切换主题


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "云控管理系统"  # 设置站点标题
    site_footer = "风擎科技"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠，在左侧，默认的
    apps_icons = {'app_d':'fa fa-cloud-download','data_statistics':'fa fa-trash-o','function_settings':'fa fa-cogs',
                  'system_setup':'fa fa-tags','talk':'fa fa-weibo'
                  }


xadmin.site.register(views.CommAdminView, GlobalSettings)


class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'remaining_accounts', 'account_num', 'date_joined', 'get_over_date']
    exclude = ['first_name', 'last_name', 'email', 'date_joined', 'last_login', 'remaining_accounts', ]
    ordering = ['id']

    def queryset(self):
        qs = super(UserAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(id=self.request.user.id)

    def save_models(self):
        if '/user/add/' in self.request.path:
            self.new_obj.remaining_accounts = self.new_obj.account_num
            self.new_obj.is_staff = True
            self.new_obj.over_time = time.time() + 3600
            super(UserAdmin, self).save_models()
            the_user = User.objects.filter(id=self.new_obj.id)
            if the_user.exists():  # 判断用户是否存在
                group = Group.objects.all()  # 添加到权限组
                if group:
                    group[0].user_set.add(self.new_obj)
        else:
            user = self.org_obj
            user.over_time = user.over_time + user.increase_time * 24 * 60 * 60
            user.increase_time = 0
            user.remaining_accounts = int(user.account_num) - len(Account_manage.objects.filter(user=user))
            super(UserAdmin, self).save_models()


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)


class AccountManageAdmin(object):
    list_display = ['id', 'account_name', 'password', 'function_setup', 'date_joined', 'status', 'equipment_id']
    ordering = ['id']
    # exclude = ['user', 'date_joined']
    list_editable = ['status', 'function_setup']
    readonly_fields = ['account_name', 'password', 'date_joined', 'equipment_id']
    # 设置多对多关系成多选框 #checkbox-inline
    style_fields = {'function_setup': 'checkbox-inline'}

    def get_model_form(self, **kwargs):  # 动态展示详情和可修改的字段
        if self.request.user.is_superuser:  # 当登录用户为admin时， 将exclude重新赋值
            self.exclude = ['user', 'date_joined']
            form = super(AccountManageAdmin, self).get_model_form()
            return form
        else:
            if '/account_manage/add/' in self.request.path:
                self.exclude = ['user', 'date_joined']
                form = super(AccountManageAdmin, self).get_model_form()
                return form
            else:
                self.exclude = ['user']
                return super(AccountManageAdmin, self).get_model_form()

    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.request.user.is_superuser:
            self.readonly_fields = []
        else:
            if '/account_manage/add/' in self.request.path:  # 判断是否是创建新用户
                self.readonly_fields = ['equipment_id']
            else:
                self.readonly_fields = ['account_name', 'password', 'date_joined', 'equipment_id']
        return self.readonly_fields

    def formfield_for_dbfield(self, db_field, **kwargs):  # 多对多的数据进行筛选
        if not self.request.user.is_superuser:  # 判断当前用户是否为超级用户，
            if db_field.name == "talk":  # 当表字段为外键字段时，对显示的数据进行过滤
                kwargs["queryset"] = Talk_manage.objects.filter(user=self.request.user)
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))
        else:
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))

    def queryset(self):
        qs = super(AccountManageAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)

    def save_models(self):
        if '/account_manage/add/' in self.request.path:
            account_num = self.user.account_num
            account_count = len(Account_manage.objects.filter(user=self.user))
            if account_count >= int(account_num):  # 判断账号是否达到上限
                self.request.META['bad'] = 1
                self.message_user('不能再添加新账号,请联系管理员', 'error')  # 使用message_user(错误信息,'error') 来生成提示信息
            else:
                obj = self.new_obj
                self.new_obj.user = self.request.user  # 关联对象默认当前用户
                super(AccountManageAdmin, self).save_models()
                self.message_user('添加信息成功', 'success')
        else:
            super(AccountManageAdmin, self).save_models()

    def save_related(self):  # 重写设置多对多关系的方法
        bad = self.request.META.get('bad', None)
        if not bad:  # bad为None时，说明操作操作成功
            self.form_obj.save_m2m()


xadmin.site.register(Account_manage, AccountManageAdmin)
