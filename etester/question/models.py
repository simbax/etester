#coding:utf-8
import cPickle as pickle

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from question.answer import SingleChoiceAnswerForm, MultiChoiceAnswerForm, FillBlankAnswerForm, TrueFalseAnswerForm

# Create your models here.


class QuestionBank(models.Model):
    name = models.CharField('题库名称', max_length=100)
    subject = models.CharField('课程名称',max_length=100)
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    question_count = models.IntegerField(default=0)
    question_checked_count = models.IntegerField(default=0)
    paper_count = models.IntegerField(default=0)
    paper_checked_count = models.IntegerField(default=0)
    paper_published_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-updated_time',]
        get_latest_by = 'updated_time'
        verbose_name_plural = '<banks>题库'
        verbose_name = '<bank>题库'

    def __unicode__(self):
        return self.name


    #Question methods
    def get_all_questions(self):
        return self.question_set.all()

    def get_checked_questions(self):
        return self.question_set.filter(is_checked=True)
    
    def get_unchecked_questions(self):
        return self.question_set.filter(is_checked=False)



    #Paper methods

    def get_all_paper(self):
        return self.exampaper_set.filter(is_visible=True)

    def get_checked_paper(self):
        return self.exampaper_set.filter(is_visibale=True,is_checked=True)

    def get_unchecked_paper(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=False)

    def get_published_paper(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=True,is_published=True)

    def get_unpublished_papes(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=True,is_published=False)

    #URL to do
    def get_all_question_list_url(self):
        return reverse('exam.views.all_question_list_view',kwargs={'bank_id':self.pk})

    def get_all_paper_list_url(self):
        return reverse('exam.views.all_paper_list_view',kwargs={'bank_id':self.pk})

    def get_add_base_info_paper_url(self):
        return reverse('exam.views.base_info_paper_view',kwargs={'bank_id':self.pk})


question_level_choices = (
                (1,'简单'),
                (2,'一般'),
                (3,'难'),
                (4,'很难'),
)
question_type_choices = (
                (1,'单项选择题'),
                (2,'多项选择题'),
                (3,'判断题'),
                (4,'填空题'),
 )

class Question(models.Model):
    bank = models.ForeignKey(QuestionBank)
    qcon = models.TextField('题干（试题内容）')
    qask = models.TextField('选项/提问', null=True, blank=True)
    qkey = models.TextField('参考答案')
    qscore = models.IntegerField('本题分数')
    qchapter = models.CharField(verbose_name='问题所属章节',max_length=100)
    qlevel = models.IntegerField('问题难度系数',choices=question_level_choices)
    qtype = models.IntegerField(choices=question_type_choices)
    qexp = models.TextField('答案解析')
    user = models.ForeignKey(User,verbose_name='作者/编者')
    is_checked = models.BooleanField('通过审核',default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    class Meta:
        get_latest_by=['updated_time',]
        ordering = ['-updated_time']
        verbose_name_plural = '试题'
        verbose_name = '试题'
     
    def __unicode__(self):
        if len(self.qcon)>20:
            self.qcon=self.qcon[:20]+'...'
        return self.qcon

    def get_paper(self):
        return self.exampaper_set.filter(is_visible=True)

    #url todo
    def get_check_url(self):
        return reverse('exam.views.question_checked_view',kwargs={'q_id':self.pk})

    def get_uncheck_url(self):
        return reverse('exam.views.question_uncheck_view',kwargs={'q_id':self.pk})
    
    def get_change_question_url(self):
        return reverse('exam.views.change_question_view',kwargs={'q_id':self.pk})

    def get_ask(self):
        if self.qask:
            value = pickle.loads(self.qask.encode())
            return value
    def get_answer_form(self,data=None, *args, **kwargs):
        if self.qtype == 1:
            return SingleChoiceAnswerForm(options=self.get_ask(),data=data,*args,**kwargs)
        elif self.qtype == 2:
            return MultiChoiceAnswerForm(options=self.get_ask(),data=data,*args,**kwargs)
        elif self.qtype == 4:
            return FillBlankAnswerForm(data=data,*args,**kwargs)
        elif self.qtype == 3:
            return TrueFalseAnswerForm(data=data,*args,**kwargs)
        else:
            pass
    
    def check_answer(self, user_key):
        if self.qtype == 1 or self.qtype == 2 or self.qtype == 3:
            if self.qkey == user_key:
                return 'True'
            elif self.qkey == unicode(user_key):
                return 'True'
            else:
                return 'False'
        else:
            return 'None'
    def get_exer_question_url(self):
        return reverse('question.views.question_view',kwargs={'q_id':self.pk})

