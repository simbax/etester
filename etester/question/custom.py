#coding:utf-8
import cPickle as pickle

from django.forms import MultiValueField, CharField, ModelMultipleChoiceField
from django.forms import MultiWidget, Textarea

class OptionsWidget(MultiWidget):
    def __init__(self, option_count=4, attrs=None):
        widgets = []
        self.option_count = option_count
        for i in range(self.option_count):
            widgets.append(Textarea(attrs=attrs))
        super(OptionsWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            value=pickle.loads(value.encode())
            return [i[1] for i in value]
        else:
            return ['' for i in range(self.option_count)]

class OptionsField(MultiValueField):

    def __init__(self, option_count=4,widget=None, *args, **kwargs):
        fields=[]
        for i in range(option_count):
            fields.append(CharField())
        widget =widget or OptionsWidget(option_count)
        super(OptionsField, self).__init__(fields, widget=widget, *args, **kwargs)

    def compress(self, data_list):
        data_list=[[chr(i+65),data_list[i]] for i in range(len(data_list))]
        return pickle.dumps(data_list)



