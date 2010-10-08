#coding: utf-8
import cPickle as pickle

from django.forms import MultiWidget,Textarea

class OptionsWidget(MultiWidget):
    def __init__(self, num=4, attrs=None):
        self.num=num
        widgets=[]
        for i in range(self.num):
            widgets.append(Textarea)
        super(OptionsWidget, self).__init__(widgets, attrs)
            
    def decompress(self, value):
        if value:
            value=pickle.loads(value.encode())
            
            return [i[1] for i in value]
        else:
            return ['' for i in range(self.num)]
