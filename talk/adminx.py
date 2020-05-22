import xadmin
from .models import Talk_manage, Weibo_manage, Commentary, Retransmission
from users.models import Account_manage


class Talk_manageAdmin(object):
    list_display = ['id', 'talk_content', 'status', 'date_joined']
    list_editable = ['status']
    ordering = ['id']
    exclude = ['user']

    def formfield_for_dbfield(self, db_field, **kwargs):  # 多对多的数据进行筛选
        if not self.request.user.is_superuser:  # 判断当前用户是否为超级用户，
            if db_field.name == "account":  # 当表字段为外键字段时，对显示的数据进行过滤
                kwargs["queryset"] = Account_manage.objects.filter(user=self.request.user)
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))
        else:
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))

    def save_models(self):
        self.new_obj.user = self.request.user
        super(Talk_manageAdmin, self).save_models()

    def queryset(self):
        qs = super(Talk_manageAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)


xadmin.site.register(Talk_manage, Talk_manageAdmin)


class Weibo_manageAdmin(object):
    list_display = ['id', 'weibo_account', 'status', 'date_joined']
    list_editable = ['status']
    exclude = ['user', 'account_manage']
    ordering = ['id']

    def formfield_for_dbfield(self, db_field, **kwargs):  # 多对多的数据进行筛选
        if not self.request.user.is_superuser:  # 判断当前用户是否为超级用户，
            if db_field.name == "account":  # 当表字段为外键字段时，对显示的数据进行过滤
                kwargs["queryset"] = Account_manage.objects.filter(user=self.request.user)
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))
        else:
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))

    def save_models(self):
        self.new_obj.user = self.request.user
        super(Weibo_manageAdmin, self).save_models()

    def queryset(self):
        qs = super(Weibo_manageAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)


xadmin.site.register(Weibo_manage, Weibo_manageAdmin)


class CommentaryAdmin(object):
    list_display = ['id', 'comment_content', 'date_joined']
    ordering = ['id']
    exclude = ['user']

    def formfield_for_dbfield(self, db_field, **kwargs):  # 多对多的数据进行筛选
        if not self.request.user.is_superuser:  # 判断当前用户是否为超级用户，
            if db_field.name == "account":  # 当表字段为外键字段时，对显示的数据进行过滤
                kwargs["queryset"] = Account_manage.objects.filter(user=self.request.user)
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))
        else:
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))

    def queryset(self):
        qs = super(CommentaryAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)

    def save_models(self):
        self.new_obj.user = self.request.user
        super(CommentaryAdmin, self).save_models()


xadmin.site.register(Commentary, CommentaryAdmin)


class RetransmissionAdmin(object):
    list_display = ['id', 'forward_content', 'date_joined']
    ordering = ['id']
    exclude = ['user']

    def formfield_for_dbfield(self, db_field, **kwargs):  # 多对多的数据进行筛选
        if not self.request.user.is_superuser:  # 判断当前用户是否为超级用户，
            if db_field.name == "account":  # 当表字段为外键字段时，对显示的数据进行过滤
                kwargs["queryset"] = Account_manage.objects.filter(user=self.request.user)
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))
        else:
            attrs = self.get_field_attrs(db_field, **kwargs)
            return db_field.formfield(**dict(attrs, **kwargs))

    def queryset(self):
        qs = super(RetransmissionAdmin, self).queryset()
        if self.request.user.is_superuser:  # 超级用户可查看所有数据
            return qs
        else:
            return qs.filter(user=self.request.user)

    def save_models(self):
        self.new_obj.user = self.request.user
        super(RetransmissionAdmin, self).save_models()


xadmin.site.register(Retransmission, RetransmissionAdmin)
