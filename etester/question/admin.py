#coding:utf-8

from django.contrib import admin


from question.models import QuestionBank, Question
from question.forms import QuestionForm, SingleChoiceForm, MultiChoiceForm, TrueFalseForm,FillBlankForm, get_question_form_class,get_question_form_fields

class QuestionBankAdmin(admin.ModelAdmin):
    exclude = ['question_count','question_checked_count',
                'paper_count','paper_checked_count',
                'paper_published_count','user']
    list_display = ('name','subject','question_count',
                    'question_checked_count','paper_count',
                    'paper_checked_count','paper_published_count',
                    'user','created_time')
    list_filter = ('subject',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
    

admin.site.register(QuestionBank, QuestionBankAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qcon','bank','qtype','qchapter','is_checked','user','created_time')
    list_filter = ['bank','qtype']
    search_fields = ['qcon',]
    change_list_template = 'admin/question/change_list.html'
#TODO:没有实现选择题选项的动态增加;
# 通过动态修改self.fields属性实现审核权限的分配。
    def get_form(self, request, obj=None, **kwargs):
        url_dict = request.GET
        q_type = url_dict.get('q_type','1')
        if obj:
            q_type =str(obj.qtype)
        self.fields = get_question_form_fields(q_type=q_type)
        if request.user.is_superuser:
            self.fields.append('is_checked')
        self.form = get_question_form_class(q_type=q_type)
        return super(QuestionAdmin, self).get_form(request,obj,**kwargs)

    def queryset(self, request):
        user = request.user
        if user.is_superuser:
            return super(QuestionAdmin,self).queryset(request)
        else:
            qs = Question.objects.filter(user=user)
            return qs

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.qtype = int(request.GET.get('q_type', obj.qtype))
        obj.save()
admin.site.register(Question, QuestionAdmin)
