#coding:utf-8


from django.forms import MultiValueField, CharField, ModelMultipleChoiceField
from django.forms import MultiWidget


class PaperAnswerField(MultiValueField):
    def __init__(self, obj=None, *args, **kwargs):
        pass
