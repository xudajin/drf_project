import xadmin
from .models import Douyin_setup, User_link_setup, Backend_setup, Culture_account
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, Side, Field

class Douyin_setupAdmin(object):
    list_display = ['id', 'title', 'key', 'default_value']
    ordering = ['id']


xadmin.site.register(Douyin_setup, Douyin_setupAdmin)


class User_link_setupAdmin(object):
    list_display = ['id', 'user', 'set_up', 'get_key_name', 'setup_value', 'date_joined']
    ordering = ['id']
    list_editable = ['setup_value']
    readonly_fields = ['user', 'set_up']

    def queryset(self):
        qs = super(User_link_setupAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user_id=self.request.user)

    def get_readonly_fields(self):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if self.request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


xadmin.site.register(User_link_setup, User_link_setupAdmin)


class Backend_setupAdmin(object):
    list_display = ['id', 'title', 'key_word', 'value', 'date_joined']
    ordering = ['id']


xadmin.site.register(Backend_setup, Backend_setupAdmin)


class Culture_accountAdmin(object):
    list_display = ['id', 'limit_watch', 'watch_duration_min', 'watch_duration_max', 'watch_times', 'date_joined']
    exclude = ['user']
    ordering=['id']

    form_layout = (
        Main( #中心内容
            Fieldset('常规设置',
                     Row('limit_watch', 'watch_duration_min', 'watch_duration_max')
                     ),
            Fieldset('随机时间暂停',
                     Row('watch_times', 'pause_time_min', 'pause_time_max')
                     ),

            Fieldset('评论区功能',
                     Row('comment_nice_probability', 'comment_nice_min_times', 'comment_nice_max_times')
                     ),
            Fieldset('关注作者',
                     Row('follow_author_probability', 'follow_author_pause_time_min', 'follow_author_pause_time_max')
                     )
        ),
        Side(  #侧边框
            Fieldset('点赞及评论概率',
                     Row('nice_probability', 'comment_probability')
                     ),
            Fieldset('转发概率',
                     Row('forward_probability')
                     ),
        )
    )

    def queryset(self):
        qs = super(Culture_accountAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user_id=self.request.user)

    def save_models(self):
        self.new_obj.user = self.request.user
        super(Culture_accountAdmin, self).save_models()

xadmin.site.register(Culture_account, Culture_accountAdmin)