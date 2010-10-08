#conding:utf-8
from django.contrib import admin
from exam.models import QuestionBank, Question, ExamPaper, AnswerSheet
from exam.views import add_question_view, change_question_view

from django.conf.urls.defaults import patterns, url

class QuestionBankAdmin(admin.ModelAdmin):
    pass
admin.site.register(QuestionBank, QuestionBankAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qcon','qtype', 'qscore', 'qlevel',)
    list_editable = ('qscore','qlevel')
    list_filter = ('qtype','qlevel')

    def get_urls(self):
        urls = super(QuestionAdmin, self).get_urls()
        q_urls = patterns('',
            url(r'^add/(?P<q_type>\d+)/$',
                 self.admin_site.admin_view(add_question_view),
                 {'template':'exam/question.html',}),
            url(r'^edit/(?P<q_id>\d+)/$',
             self.admin_site.admin_view(change_question_view),
                 {'template':'exam/question.html',}),
                          )
        return q_urls + urls
    

admin.site.register(Question, QuestionAdmin)

admin.site.register(ExamPaper)

admin.site.register(AnswerSheet)
