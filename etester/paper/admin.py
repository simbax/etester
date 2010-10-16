#coding:utf-8

from django.core.urlresolvers import resolve
from django.contrib.admin import site
from django.contrib import admin

from paper.models import QuestionBank, Question, ExamPaper, PaperConfig

class PaperConfigInline(admin.TabularInline):
    model = PaperConfig
    verbose_name = "配置试题"
    verbose_name_plural = '配置试题'
    extra = 1
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            bank = QuestionBank.objects.get(pk=request.GET['bank_id'])
        except:
            paper_id = resolve(request.path)[1][0]
            bank = ExamPaper.objects.get(pk=paper_id).bank
        if db_field.name == 'question':
            kwargs['queryset'] = Question.objects.filter(bank=bank,is_checked=True)
        return super(PaperConfigInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ExamPaperAdmin(admin.ModelAdmin):
    exclude = ['user','total_score','status','bank']
    inlines = [PaperConfigInline,]
    list_display = ['name','set_name','set_no','bank','paper_type','total_score','user','is_checked','is_published']
    def queryset(self, request):
        qs = super(ExamPaperAdmin, self).queryset(request).filter(is_visible=True)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if change == False:
            obj.bank = QuestionBank.objects.get(pk=request.GET['bank_id'])
        obj.save()


site.register(ExamPaper, ExamPaperAdmin)
