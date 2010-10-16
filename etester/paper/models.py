#coding:utf-8


from django.db import models
from django.contrib.auth.models import User

from question.models import QuestionBank, Question



# Create your models here.


paper_type_choices = ((1,'考试试卷'),
                    (2,'自测试卷'),
                    )
paper_status = ((1,'试卷已创建'),
                (2,'试题已设定'),
                (3,'试题排序，分值已设定'),
                (4,'组卷完成'))

class ExamPaper(models.Model):
    name = models.CharField('试卷名称', max_length=100, help_text=u"长度不能超过100个字符。")
    set_name = models.CharField('试卷集名称',max_length=100,blank=True,null=True)
    set_no = models.IntegerField('试卷集编号',default=0)
    user = models.ForeignKey(User)
    questions = models.ManyToManyField(Question,null=True,blank=True,through='PaperConfig')
    total_score = models.IntegerField('总分', default=0)
    paper_type = models.IntegerField('试卷类型',choices=paper_type_choices)
    bank = models.ForeignKey(QuestionBank)
    is_checked = models.BooleanField('审核通过',default=False)
    #发布后禁止修改，因为可能有人已经使用这个试卷答卷了。
    is_published = models.BooleanField('发布试卷', default=False)
    #删除发布后的试卷
    is_visible = models.BooleanField('有效', default=True,help_text = u'未选中即删除')
    status = models.IntegerField('试卷状态', default=0, choices=paper_status)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '试卷'
        verbose_name = '试卷'
        ordering=['-updated_time']
        get_latest_by=['updated_time']
    
    def __unicode__(self):
        return '%s<%s,%s>' % (self.name, self.set_no, self.set_name)
    def save(self):
        qs = PaperConfig.objects.filter(paper=self)
        self.total_score = 0
        for i in qs:
            if i.score:
                self.total_score += i.score
            else:
                self.total_score += i.question.qscore
        super(ExamPaper, self).save()


class PaperConfig(models.Model):
    paper = models.ForeignKey(ExamPaper,blank=True,null=True)
    question = models.ForeignKey(Question,blank=True,null=True)
    score = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['paper','order','question']

    def __unicode__(self):
        return u'%s Config' % self.paper
