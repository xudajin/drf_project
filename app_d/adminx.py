import xadmin
from .models import Control_download, Appdownload
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, Side, Field

class Control_downloadAdmin(object):
    list_display = ['id', 'title', 'download','date_joined']
    list_editable=['download']
    ordering=['id']


xadmin.site.register(Control_download, Control_downloadAdmin)


class AppdownloadAdmin(object):
    list_display = ['id', 'title', 'download','date_joined']
    list_editable = ['download']
    ordering=['id']

    form_layout = (
            Fieldset('',
                     Row('title',),
                     Row('app_file',),
                     Row('download',),
                     Row('remarks')
                     ),
    )

xadmin.site.register(Appdownload, AppdownloadAdmin)
