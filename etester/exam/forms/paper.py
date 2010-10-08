#coding:utf-8

from django import forms
from django.forms import ModelForm

from exam.models import ExamPaper, ExamConfig
from fields import ModelMultipleQuestionsField
class BaseInfoPaperForm(ModelForm):

    class Meta:
        model = ExamPaper
        exclude = ('questions','total_score','bank','is_checked','is_publish','is_visible','status','is_completed','create_time','updated_time')


class ArtificialSelectPaperForm(forms.Form):
    def __init__(self,qs=None):
        self.fields['questions'] = forms.ModelMultipleQuestionsField(queryset=qs,
                                                    widget=forms.CheckboxSelectMultiple)

        
        
class QuestionOrderPaperForm(ModelForm):
    class Meta:
        model = ExamConfig
        exclude = ('paper','question',)
class CheckedPaperForm(forms.Form):
    pass

class PublishPaperForm(forms.Form):
    pass

