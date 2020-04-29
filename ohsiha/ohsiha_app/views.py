from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice, Ans, ExternalKoronaData
from .visualization import make_barchart, make_linegraph, make_user_data_linegraph
from django.views  import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.utils import timezone
import requests
import datetime
import json
from django.contrib.auth.models import User


#Class for checking if user is admin
class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'ohsiha_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'ohsiha_app/detail.html'

class ResultsView(AdminStaffRequiredMixin, generic.DetailView):
    model = Ans
    template_name = 'ohsiha_app/results.html'
    permission_denied_message = "You are not allowed here."
    def all_inputs(self):
        return Ans.objects.all()

def result_helper(request, user_id):
    script = []
    div = []
    if request.user.is_superuser or request.user.is_staff:
        #users = Ans.objects.values('respondent_name').distinct()
        users = User.objects.values('username').distinct()
        try:
            filtered_data = Ans.objects.filter(user_id = user_id)
            script, div = make_user_data_linegraph(filtered_data)
        except(...):
            return render(request, 'ohsiha_app/results.html')

        context= {
                'all_answers': filtered_data, 
                'users' : users,
                'script' : script,
                'div' : div}

        return render(request, 'ohsiha_app/results.html', context)
    else:
        return render(request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})    

def show_all_answers(request):
    script = []
    div = []
    if request.user.is_superuser or request.user.is_staff:
        all_answers = Ans.objects.all()

        script, div = make_user_data_linegraph(all_answers)

        users = User.objects.values('username').distinct()

        context= {
        'all_answers': all_answers, 
        'users' : users, 
        'script': script,
        'div' : div,}

        return render(request, 'ohsiha_app/results.html', context)
    else:
        return render(request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ohsiha_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        current_user = request.user
        response = Ans()
        response.respondent_name = current_user
        response.question = question
        response.choise = selected_choice
        response.date = timezone.now()
        response.user_id = current_user.id
        response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        if (Question.objects.filter(id = question.id + 1)).exists():
            return HttpResponseRedirect(reverse('ohsiha_app:detail', args=(question.id + 1,)))
        else:
            return HttpResponseRedirect(reverse('ohsiha_app:index'))    

def home(request):
    script = []
    div = []

    if not ExternalKoronaData.objects.filter(pull_date = timezone.now()).exists():
        e = ExternalKoronaData.objects.create()
        e.pull_data_from_api()
        e.save()

    else:
        e = ExternalKoronaData.objects.get(pull_date = timezone.now())

    conf_amount = e.conf_amount
    reco_amount = e.reco_amount

    script, div = make_barchart(e)
    script2, div2 = make_linegraph(e)

    return render(request, 'ohsiha_app/home.html', {
        'confirmed':  conf_amount,
        'recovered':  reco_amount,
        'script': script,
        'div' : div,
        'script2' : script2,
        'div2' : div2
    })

def coach_home(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'ohsiha_app/coach_home.html')
    else:
        message = "Tämä alue on vain valmentajille."
        return (request, 'ohsiha_app/denied.html', {
                'message': message})
      
def add_question(request):
    if request.user.is_superuser or request.user.is_staff:
        kysymykset = Question.objects.all()
        if request.method == 'POST':
            q = Question(question_text=request.POST['qtext'], pub_date=timezone.now())
            q.save()
            if len(request.POST['atext']) >  0:
                choises = request.POST['atext'].split(';')
                i = 0
                for choice in choises:
                    q.choice_set.create(choice_text=choice, votes=0, category = i)
                    i = i + 1
                q.save()  

        return render(request, 'ohsiha_app/add_question.html',{'kysymykset' : kysymykset})
    else:
        return (request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})    
          
def delete_question(request):
    if request.user.is_superuser or request.user.is_staff:
        kysymykset = Question.objects.all()

        if request.method == 'POST':
            q = Question.objects.get(pk=request.POST['question'])
            q.delete()
            kysymykset = Question.objects.all()
        return render(request, 'ohsiha_app/delete.html',{'kysymykset' : kysymykset})
    else:
        return (request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})   

def modify_question(request):
    if request.user.is_superuser or request.user.is_staff:
        kysymykset = Question.objects.all()

        if request.method == 'POST':
            q = Question.objects.get(pk=request.POST['question'])
            if len(request.POST['qtext']) >  0:
                q.question_text = request.POST['qtext']
                q.save()

            if len(request.POST['atext']) >  0:
                choises = request.POST['atext'].split(';')
                i = q.choice_set.count() + 1
                for choice in choises:
                    q.choice_set.create(choice_text=choice, votes=0, category = i)
                    i = i + 1
                q.save()

            kysymykset = Question.objects.all()
        return render(request, 'ohsiha_app/modify_question.html',{'kysymykset' : kysymykset})
    else:
        return (request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})       