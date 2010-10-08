#coding:utf-8
# Create your views here.
import cPickle as pickle

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404, get_list_or_404


from models import Question, ExamPaper, QuestionBank, ExamConfig
from forms import make_question_form, make_answer_question_form
from forms import BaseInfoPaperForm, ArtificialSelectPaperForm, QuestionOrderPaperForm


def all_question_list_view(request, bank_id=none):
    template = 'exam/question_list.html'
    context = {}
    bank = get_object_or_404(QuestionBank,pk=bank_id)
    qs = bank.get_all_questions()
    context['questions'] = qs
    return render_to_response(template,context)

def add_question_view(request, bank_id='1', q_type='1', num='4'):
    template = 'exam/question.html'
    context = {}
    if request.method == 'POST':
        form_class = make_question_form(q_type=q_type)
        if q_type=='1' or q_type=='2':
            form = form_class(data=request.POST,num=int(num))
        else:
            form = form_class(request.POST)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.qtype = int(q_type)
            new_obj.user = request.user
            new_obj.bank = QuestionBank.objects.get(pk=bank_id)
            new_obj.save()
        return redirect(all_question_view,bank_id=bank_id)
    else:
        form_class = make_question_form(q_type=q_type)
        if q_type=='1' or q_type=='2':
            form=form_class(num=int(num))
        else:
            form=form_class()
        context['form'] = form
        return render_to_response(template,context)


def change_question_view(request, q_id=None):
    template = 'exam/question.html'
    context = {}
    q = get_object_or_404(Question,pk=q_id)
    q_type = str(q.qtype)
    form_class = make_question_form(q_type=q_type)
    if request.method == 'POST':
        if q_type=='1' or q_type=='2':
            num = len(pickle.loads(q.qask.encode()))
            form = form_class(data=request.POST,instance=q,num=num)
        else:
            form = form_class(request.POST,instance=q)
        if form.is_valid():
            new_obj = form.save()
        return redirect('all_question_view',bank_id=q.bank.pk)
    else:
        if q_type=='1' or q_type=='2':
            num=len(pickle.loads(q.qask.encode()))
            if q_type=='2':
                q.qkey = pickle.loads(q.qkey.encode())
            form = form_class(num=num,instance=q)
        else:
            form = form_class(instance=q)
        context['form'] = form
        return render_to_response(template,context)
       
def question_checked_view(request,q_id=None):
    question = get_object_or_404(Question,pk=q_id)
    question.is_checked = True
    question.save()
    question.bank.question_checked_num +=1
    question.bank.save()
    return redirect(all_question_view,bank_id=question.bank.pk)

def question_uncheck_view(request,q_id=None):
    question = get_object_or_404(Question,pk=q_id)
    question.si_checked = False
    question.save()
    question.bank.question_checked_num -=1
    question.bank.save()
    return redirect(all_question_view,bank_id=question.bank.pk)

def quiz(request,q_id):
    q = Question.objects.filter(pk=q_id)
    pk_set = range(1)
    forms = make_answer_question_form(q)
    return render_to_response('exam/quiz.html',{'q':q,
                            'pk':pk_set,'forms':forms})
#练习模式，一问一答一比对答案，需要使用session。
def exercise_view(request,t_id):
    pass

#自测模式，全部答完之后显示参考答案。
def test_view(request,t_id):
    pass

#考试模式，
def exam_view(request, t_id):
    pass

def all_paper_list_view(request,bank_id):
    template = 'exam/paper_list.html'
    context = {}
    bank = get_object_or_404(QuestionBank,pk=bank_id)
    ps = bank.get_all_paper()
    context['papers']=ps
    return render_to_response(template,context)


#新增和修改试卷基本信息
def base_info_paper_view(request,bank_id=None,p_id=None):
    template = 'exam/base_info_paper.html'
    context = {}
    if bank_id:
        if request.method='POST':
            form = BaseInfoPaperForm(request.POST)
            if form.is_valid():
                new_obj = form.save(commit=False)
                new_obj.bank = Question.objects.get(pk=bank_id)
                new_obj.status = 1
                new_obj.save()
                return redirect(all_paper_list_view,bank_id=bank_id)
        else:
            form = BaseInfoPaperForm()
            context['form']=form
            return render_to_response(template,context)
    if p_id:
        paper = get_object_or_404(ExamPaper,pk=p_id)
        if request.methon == 'POST':
            form = BaseInfoPaperForm(request.POST,instance=paper)
            if form.is_valid():
                p_obj = form.save()
                return redirect(paper_list_view,bank_id=paper.bank.pk)
        else:
            form = BaseInfoPaperForm(instance=paper)
            context['form']=form
            return render_to_response(template,context)

def artificial_select_paper_view(request,p_id):
    template = 'exam/artificial_select_paper.html'
    conetxt = {}
    paper = get_object_or_404(ExamPaper,pk=p_id)
    select_qs = paper.questions.all()
    bank = paper.bank
    qs = bank.get_checked_questions()
    if request.method = 'POST':
        form =ArtificialSelectPaperForm(initial={'questions':select_qs},qs=qs)
        if form.is_valid():
            questions = form.cleaned_data['questions']
            if select_qs:
                paper.questions.clear()
            for q in questions:
                ExamConfig.objects.create(paper=paper,question=q)
            return redirect(all_paper_list_view,bank_id=bank.pk)
    else:
        form = ArtificialSelectPaperForm(qs=qs)
        context['form'] = form
        return render_to_response(template,context)

def question_order_paper_view(request,p_id):
    template = 'exam/question_order_paper.html'
    context = {}
    paper= get_object_or_404(ExamPaper,pk=q_id)
    forms = []
    qs = ExamConfig.objects.filter(paper=paper).order_by('order','pk')
    if request == 'POST':
        for q in qs:
            forms.append(QuestionOrderpaperForm(request.POst,prefix=q.pk,instance=q))
        for form in forms:
            if form.is_valid():
                form.save()
        return redirect(all_paper_list_view,bank_id=paper.bank.pk)
    else:
        for q in qs:
            forms.append(QuestionOrderPaperForm(prefix=q.pk,instance=q))
            context['forms'] = forms
        return render_to_response(template,context)

def paper_checked_view(request,p_id):
    p = get_object_or_404(ExamPaper,pk=q_id)
    p.is_checked = True
    p.status = 4
    p.bank.paper_checked_num += 1
    p.save()
    return redirect(all_paper_list_view,bank_id=p.bank.pk)
def paper_uncheck_view(request,p_id):
    p = get_object_or_404(ExamPaper,pk=q_id)
    p.is_checked = False
    p.status = 3
    p.bank.paper_checked_num -=1
    p.save()
    return redirect(all_paper_list_view,bank_id=p.bank.pk)

def paper_publish_view(request,p_id):
    p = get_object_or_404(ExamPaper,pk=q_id)
    p.is_published = True
    p.status = 5
    p.save()
    return redirect(all_paper_list_view,bank_id=p.bank.pk)

def paper_unpublish_view(request,p_id):
    p = get_object_or_404(ExamPaper,pk=q_id)
    p.is_published = False
    p.status = 4
    p.save()
    return redirect(all_paper_list_view,bank_id=p.bank.pk)
def delete_paper_view(request,p_id):
    p = get_object_or_404(ExamPaper,pk=q_id)
    p.is_visible = False
    p.save()
    return redirect(all_paper_list_view, bank_id=p.bank.pk)
