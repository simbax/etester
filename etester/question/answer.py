#coding:utf-8

from django import forms

_choices2 = (('True',u'正确'),
            ('False',u'错误'),)
class SingleChoiceAnswerForm(forms.Form):
    ''' for user to answer single choice question.'''
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
        self.fields['qkey']= forms.CharField( max_length=100)

class TrueFalseAnswerForm(forms.Form):
    qkey = forms.ChoiceField(widget=forms.RadioSelect, choices=_choices2)
