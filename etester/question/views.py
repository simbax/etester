#coding:utf-8
# Create your views here.

from django.shortcuts import get_object_or_404, render_to_response

from question.models import Question

def question_view(request,q_id,):
    q = get_object_or_404(Question,pk=q_id)
    context = {}
    context['q'] = q
    if request.method == 'POST':
        form = q.get_answer_form(request.POST)
        context['form'] = form
        if form.is_valid():
            q_key = form.cleaned_data['qkey']
            flag = q.check_answer(q_key)
            context['flag'] = flag
            return render_to_response('question/question.html',context)
    else:
        form = q.get_answer_form()
        context['form'] = form
        return render_to_response('question/question.html',context)




