#coding:utf-8

import cPickle as pickle


from django import forms
from django.forms import ModelForm
from django.forms.util import ErrorList

from question.models import Question, QuestionBank

from question.custom import OptionsField


_choices2 = (
            ('True',u'正确'),
            ('False',u'错误'),)
#get 2-list composed by A..Z.
def get_choices(option_count=4):
    options=[(chr(i), chr(i)) for i in range(65, 65+option_count)]
    return options


class QuestionForm(ModelForm):
    class Meta:
        model = Question

    def _media(sele):
        return forms.Media(css={'all':('css/admin/question/form.css',)},)
    media = property(_media)

class SingleChoiceForm(QuestionForm):
    def __init__(self, date=None, files=None, auto_id='id_%s', prefix=None,
                initial=None, error_class=ErrorList, label_suffix=':',
                empty_permitted=False, instance=None, option_count=4):
        super(SingleChoiceForm,self).__init__(date,files,auto_id,prefix,initial,
                                                error_class, label_suffix,empty_permitted,instance)
        self.fields['qask'] = OptionsField(option_count=option_count,label="选项A")
        self.fields['qkey'] = forms.ChoiceField(widget=forms.RadioSelect,label="参考答案",
                                                choices=get_choices(option_count=option_count))




class MultiChoiceForm(SingleChoiceForm):
    def __init__(self, date=None, files=None, auto_id='id_%s', prefix=None,
                initial=None, error_class=ErrorList, label_suffix=':',
                empty_permitted=False, instance=None, option_count=4):
        super(MultiChoiceForm,self).__init__(date,files,auto_id,prefix,initial,
                                            error_class, label_suffix,empty_permitted,instance)
        self.fields['qkey'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                label="参考答案",choices=get_choices(option_count))


    def clean(self):
        super(MultiChoiceForm, self).clean()
        self.cleaned_data['qkey']=unicode(self.cleaned_data['qkey'])
        return self.cleaned_data

class TrueFalseForm(QuestionForm):
    qkey = forms.ChoiceField(label='参考答案',widget=forms.RadioSelect, choices=_choices2)

class FillBlankForm(QuestionForm):
    pass
def get_question_form_class(q_type='1'):
    if q_type == '1':
        return SingleChoiceForm
    if q_type == '2':
        return MultiChoiceForm
    if q_type == '3':
        return TrueFalseForm
    if q_type == '4':
        return FillBlankForm

def get_question_form_fields(q_type='1'):
    fields = ['bank','qcon','qask','qkey','qscore','qlevel','qexp','qchapter']
    if q_type == '1' :
        pass
    if q_type == '2' :
        pass
    if q_type == '3' :
        fields.remove('qask')
    if q_type == '4' :
        fields.remove('qask')
    return fields


class SingleChoiceAnswerForm(forms.Form):
    def __init__(self, options=[], *args, **kwargs):
        super(SingleChoiceAnswerForm, self).__init__(*args,**kwargs)
        self.fields['qkey'] = forms.ChoiceField(widget=forms.RadioSelect,choices=options)

class MultiChoiceAnswerForm(forms.Form):
    def __init__(self, options=[], *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        self.fields['qkey'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                choices=options)

class FillBlankAnswerForm(forms.Form):
    def __init__(self,num=1,*args, **kwargs):
        super(FillBlankAnswerForm,self).__init__(*args,**kwargs)
        for i in range(num):
            self.fields['qkey']= forms.CharField( max_length=100)

class TrueFalseAnswerForm(forms.Form):
    qkey = forms.ChoiceField(widget=forms.RadioSelect, choices=_choices2)
