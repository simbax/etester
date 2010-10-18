#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

from question.models import Question
# Create your models here.



class ExamAnswer(models.Model):
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
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
       def __unicode__(self):
           return self.user+': ' + self.paper.name


class ExerciseAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.TextField()
    score = models.IntegerField('本题得分')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)




