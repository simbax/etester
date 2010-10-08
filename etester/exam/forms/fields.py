#coding: utf-8
import cPickle as pickle

from django.forms import MultiValueField, CharField, ModelMultipleChoiceField
from widgets import OptionsWidget
class OptionsField(MultiValueField):
    widget = OptionsWidget #default widget
    
    def __init__(self, num=4, *args, **kwargs):
        fields=[]
        self.num=4
        for i in range(self.num):
            fields.append(CharField())
        super(OptionsField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        data_list=[[chr(i+65),data_list[i]] for i in range(len(data_list))]
        return pickle.dumps(data_list)
            
            
class MultipleQuestionsChoiceField(ModelMultipleChoiceField):
    pass
