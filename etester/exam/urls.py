#coding:utf-8

from django.conf.urls.defaults import *




from views import *


urlpatterns = patterns('',
        (r'^question/list/(?P<bank_id>\d+/$)',all_question_list_view),
        (r'^question/add/$',add_question_view),
        (r'^question/change/$',change_question_view),
        (r'^question/check/$',question_checked_view),
        (r'^question/unchenk/$',question_uncheck_view),
        
        (r'^paper/list',),
        (r'^paper/add/$',base_info_paper_view,name=base_info_paper_view_add),
        (r'^paper/change/$',base_info_paper_view,name=base_info_paper_view_change),
        (r'^paper/select/$',),
        (r'^paper/order'),
        (r'^paper/check/',),
        (r'^paper/uncheck',),
        (r'^paper/publish'),
        (r'^paper/unpublish'),
        (r'^paper/review'),
        (r'^paper/delete/'),


        )
