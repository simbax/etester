#coding:utf-8
# Create your views here.


from django.shortcuts import render_to_response, get_object_or_404

from paper.models import ExamPaper, PaperConfig

def paper_view(request,p_id):
    context = {}
    forms = {}
    p = get_object_or_404(ExamPaper, pk=p_id)
    qs = PaperConfig.objects.filter(paper=p)
    context['qs'] = qs
    if request.method == 'POST':
        keys = {}
        answers = {}
        for i in qs:
            q_id = i.question.pk
            form = i.question.get_answer_form(request.POST, prefix=q_id)
            forms[q_id] = form
            if form.is_valid():
                q_key = form.cleaned_data['qkey']
                keys[q_id] = i.question.check_answer(q_key)
#TODO 需要将answers存储到数据库中，作为成绩进行记录。并且进一步进行主观题判卷
                answers[q_id] = [q_key,keys[q_id]]
            context['keys'] = keys
            context['forms'] = forms
        return render_to_response('paper/paper.html',context)
    else:
        for i in qs:
            form = i.question.get_answer_form(prefix=i.question.pk)
            forms[i.question.pk] = form
        context['forms'] = forms
        return render_to_response('paper/paper.html',context)
    
