import xadmin
from .models import Data_statistics

class Data_statisticsAdmin(object):
	list_display=['id','account_id','function_type','total_number','write_day','date_joined']
	ordering=['id']
	list_filter=['account_id','function_type']
	search_fields=['account_id','function_type']
	def queryset(self):
		qs = super(Data_statisticsAdmin, self).queryset()
		if self.request.user.is_superuser:  # 超级用户可查看所有数据
			return qs
		else:
			id_list =[i.id for i in self.request.user.account.all()]
			if id_list:
				return qs.filter(account_id__in=id_list)
			else:
				return qs.none()


xadmin.site.register(Data_statistics,Data_statisticsAdmin)

