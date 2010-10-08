#coding:utf-8
import cPickle as pickle

from django import forms
from django.forms import ModelForm
from exam.models import Question, QuestionBank
from fields import OptionsField
from widgets import OptionsWidget




_choices2 = (
        ('True',u'正确'),
        ('False',u'错误'),)
#get 2-list composed by A..Z.
def get_choices(num=4):
    options=[(chr(i),chr(i)) for i in range(65,65+num)]
    return options
    

class QuestionForm(ModelForm):
    ''' Base question class, display the shared fields
    '''

    class Meta:
        model = Question
        exclude = ('bank', 'qtype','user','is_checked','created_time','updated_time')

class SingleChoiceForm(QuestionForm):
    def __init__(self,num=4,*args,**kwargs):
        super(SingleChoiceForm,self).__init__(*args,**kwargs)
        self.fields['qask']=OptionsField(num=num, widget=OptionsWidget(num=num))
        self.fields['qkey'] = forms.ChoiceField(widget=forms.RadioSelect, choices=get_choices(num))

class MultiChoiceForm(QuestionForm):
    def __init__(self,num=4,*args,**kwargs):
        self.num=num
        super(MultiChoiceForm,self).__init__(*args,**kwargs)
        self.fields['qask'] = OptionsField(num=self.num, widget=OptionsWidget(num=self.num))
        self.fields['qkey'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                            choices=get_choices(self.num))

    def clean(self):
        super(MultiChoiceForm, self).clean()
        self.cleaned_data['qkey']=pickle.dumps(self.cleaned_data['qkey'])
        return self.cleaned_data

class TrueFalseForm(QuestionForm):
    qkey = forms.ChoiceField(label='question answer',
                             widget=forms.RadioSelect, choices=_choices2)
    class Meta(QuestionForm.Meta):
        exclude = ('bank','qask','qtype','user','is_checked','created_time','updated_time')

class FillBlankForm(QuestionForm):
    qcon = forms.CharField(widget=forms.Textarea,
                           help_text='## represent blank')
    qkey = forms.CharField(label='question answer', max_length=1000)
    
    class Meta(QuestionForm.Meta):
        exclude = ('bank','qask','qtype','user','is_checked','created_time','updated_time')


def make_question_form(q_type='1'):

    if q_type == '1':
        return SingleChoiceForm
    if q_type == '2':
        return MultiChoiceForm
    if q_type == '3':
        return TrueFalseForm
    if q_type == '4':
        return FillBlankForm
    




class SingleChoiceAnswerForm(forms.Form):
    def __init__(self, options=[], *args, **kwargs):
        super(SingleChoiceAnswerForm, self).__init__(*args,**kwargs)
        self.fields['qkey'] = forms.ChoiceField(widget=forms.RadioSelect,choices=options)
        
class MultiChoiceAnswerForm(forms.Form):
    def __init__(self, options=[], *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        self.fields['qkey'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=options)

class FillBlankAnswerForm(forms.Form):
    def __init__(self,num=1,*args, **kwargs):
        super(FillBlankAnswerForm,self).__init__(*args,**kwargs)
        for i in range(num):
            self.fields['qkey']= forms.CharField( max_length=100)

class TrueFalseAnswerForm(forms.Form):
    qkey = forms.ChoiceField(widget=forms.RadioSelect, choices=_choices2)


def make_answer_question_form(objs=[]):
    objs=objs
    forms=[]
    if objs:
        for i in objs:
            q_type=str(i.qtype)
            if q_type=='1':
                ops=eval(i.qask)
                forms.append(SingleChoiceAnswerForm(options=ops,prefix=i.pk))
            if q_type=='2':
                ops=eval(i.qask)
                forms.append(MultiChoiceAnswerForm(options=ops,prefix=i.pk))
            if q_type=='3':
                forms.append(TrueFalseAnswerForm(prefix=i.pk))
            if q_type=='4':
                num=1 #添加多个空的功能 
                forms.append(FillBlankAnswerForm(num=num,prefix=i.pk))
    #else:加入异常处理
    return forms
        



