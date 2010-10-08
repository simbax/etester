#coding:utf-8

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your models here.

class QuestionBank(models.Model):
    name = models.CharField(_('bank name'), max_length=100)
    subject = models.CharField(_('subject'),max_length=100)
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    question_num = models.IntegerField(default=0)
    question_checked_num = models.IntegerField(default=0)
    paper_num = models.IntegerField(default=0)
    paper_checked_num = models.IntegerField(default=0)
    paper_published_num = models.IntegerField(default=0)
    class Meta:
        ordering = ['-updated_time',]
        get_latest_by = 'updated_time'
        verbose_name_plural = '题库表'
        verbose_name = '题库表'
    def __unicode__(self):
        return self.name


    #获取该库所有试题
    def get_all_questions(self):
        return self.question_set.all()
    #获取审核后的试题
    def get_checked_questions(self):
        return self.question_set.filter(is_checked=True)
    def get_unchecked_questions(self):
        return self.question_set.filter(is_checked=False)
    #获取试卷，
    def get_all_paper(self):
        return self.exampaper_set.filter(is_visible=True)
    def get_checked_paper(self):
        return self.exampaper_set.filter(is_visibale=True,is_checked=True)
    def get_unchecked_paper(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=False)
    def get_published_paper(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=True,is_publish=True)
    def get_unpublished_papes(self):
        return self.exampaper_set.filter(is_visible=True,is_checked=True,is_publish=False)
   #获取删除的试卷
    def get_delete_paper(self):
        return self.exampaper_set.filter(is_visible=False)
    
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
    '''
        question model
    '''
    bank = models.ForeignKey(QuestionBank)
    qcon = models.TextField(_('question content'))
    qask = models.TextField(_('question ask'), null=True, blank=True)
    qkey = models.TextField(_('question key'), )
    qscore = models.IntegerField(_('question score'))
    qchapter = models.CharField(verbose_name='question chapter',max_length=100)
    qlevel = models.IntegerField(_('question level'),choices=question_level_choices)
    qtype = models.IntegerField(_('question type'), choices=question_type_choices)
    qexp = models.TextField(_('question explain'))
    user = models.ForeignKey(User,verbose_name=_('add person/designer'))
    is_checked = models.BooleanField(_('is  checked'),default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by=['updated_time',]
        ordering = ['-updated_time']
        verbose_name_plural = '试题库'


    def __unicode__(self):
        if len(self.qcon)>20:
            self.qcon=self.qcon[:20]+'...'
        return self.qcon

    def get_paper(self):
        return self.exampaper_set.filter(is_visible=True)

    def get_check_url(self):
        return reverse('exam.views.question_checked_view',kwargs={'q_id':self.pk})
    
    def get_uncheck_url(self):
        return reverse('exam.views.question_uncheck_view',kwargs={'q_id':self.pk})
    def get_change_question_url(self):
        return reverse('exam.views.change_question_view',kwargs={'q_id':self.pk})


    

    

paper_type_choices = (
                    (1,'章节练习'),
                    (2,'自测练习'),
                    (3,'考试试卷'),)
paper_status = (
                (1,'试卷已创建'),
                (2,'选择试题'),
                (3,'排列顺序'),
                (4,'审核发布'),
                (5,'完成组卷'),)
                
class ExamPaper(models.Model):
    name = models.CharField(_('exam paper name'), max_length=100)
    set_name = models.CharField(_('set name'),max_length=100,blank=True,null=True)
    set_no = models.IntegerField(_('Set No.'),default=0)
    questions = models.ManyToManyField(Question,null=True,blank=True,through='ExamConfig')
    total_score = models.IntegerField(_('exam paper total score'),default=0)
    paper_type = models.IntegerField(choices=paper_type_choices)
    bank = models.ForeignKey(QuestionBank)
    is_checked = models.BooleanField(default=False)
    #发布后禁止修改，因为可能有人已经使用这个试卷答卷了。
    is_published = models.BooleanField(default=False)
    #删除发布后的试卷
    is_visible = models.BooleanField(default=True)
    status = models.IntegerField(default=0,choices=paper_status)
    is_completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '试卷表'
        verbose_name = '试卷表'
        ordering=['-updated_time']
        get_latest_by=['updated_time']

    def __unicode__(self):
        return self.name
    
    def get_all_answers(self):
        return self.answersheet_set.all()

    def get_test_answers(self):
        return self.answersheet_set.filter(is_test=True)
    def get_exercise_answers(self):
        return self.answersheet_set.filter(is_exercise=True)
    def get_change_base_info_paper_url(self):
        return reverse('exam.views.base_info_paper_view',kwargs={'p_id':self.pk})
    def get_question_order_paper_url(self):
        return reverse('exam.views.question_order_paper_view',kwargs={'p_id':self.pk})
    def get_artificial_select_paper_url(self):
        return reverse('exam.views.artifivial_select_paper_view',kwargs={'p_id':self.pk})
    def get_check_url(self):
        return reverse('exam.views.paper_checked_view',kwargs={'p_id':self.pk})
    def get_uncheck_url(self):
        return reverse('exam.views.paper_uncheck_view',kwargs={'p_id':self.pk})
    def get_publish_url(self):
        return reverse('exam.views.paper_publish_view',kwargs={'p_id':self.pk})
    def get_unpublish_url(self):
        return reverser('exam.views.paper_unpublish_view',kwargs={'p_id':self.pk})
    def get_review_url(self):
        return reverse('exam.views.paper_review_view',kwargs={'p_id':self.pk})
class ExamConfig(models.Model):
    paper = models.ForeignKey(ExamPaper,blank=True,null=True)
    question = models.ForeignKey(Question,blank=True,null=True)
    score = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['paper','order','question']

class AnswerSheet(models.Model):
    paper = models.ForeignKey(ExamPaper)
    user = models.ForeignKey(User)
    answers = models.TextField(_('answer set'))
    scores = models.TextField(_('score set'))
    total_score = models.IntegerField(_('score'),default=0)
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    use_time = models.CharField(_('used time'), max_length=100,blank=True,null=True)
    on_line = models.BooleanField(_('on line'))
    finished = models.BooleanField(_('finished?'))
    force_time = models.DateTimeField(_('force time'))
    is_test = models.BooleanField(default=False)
    is_exercise = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user+': ' + self.paper.name
