#coding:utf-8
from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^etester/', include('etester.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^exam/', include(exam.urls)),
    #(r'^q/add/(?P<q_bank>\d+)/(?P<q_type>\d+)/(?P<num>\d+)/$', 'exam.views.add_question_view'),
    #(r'^q/add/(?P<q_type>\d+)/$', 'exam.views.question', {'template':'exam/question.html',}),
    #(r'^q/edit/(?P<q_id>\d+)/$', 'exam.views.change_question_view'),
    #(r'quiz/(?P<q_id>\d+)/$', 'exam.views.quiz'), 
                       
)


if settings.DEBUG == True:
	urlpatterns += patterns('',
		(r'^static/(.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	)
