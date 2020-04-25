from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice, Ans, ExternalKoronaData
from .visualization import make_barchart, make_linegraph
from django.views  import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.utils import timezone
import requests
import datetime
import json


#Class for checking if user is admin
class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'ohsiha_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


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
    if request.user.is_superuser or request.user.is_staff:
        users = Ans.objects.values('respondent_name').distinct()
        try:
            filtered_data = Ans.objects.filter(user_id = user_id)
        except(...):
            return render(request, 'ohsiha_app/results.html')

        context= {'all_answers': filtered_data, 'users' : users}
        return render(request, 'ohsiha_app/results.html', context)
    else:
        return render(request, 'ohsiha_app/denied.html', {
                'message': "Tämä alue on vain valmentajille.",})    

def show_all_answers(request):
    if request.user.is_superuser or request.user.is_staff:
        all_answers= Ans.objects.all()
        users = Ans.objects.values('respondent_name').distinct()
        context= {'all_answers': all_answers, 'users' : users}
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
        return HttpResponseRedirect(reverse('ohsiha_app:detail', args=(question.id,)))

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

@login_required
def barchart(request):

    if not ExternalKoronaData.objects.filter(pull_date = timezone.now()).exists():
        e = ExternalKoronaData.objects.create()
        e.pull_data_from_api()
        e.save()

    else:
        e = ExternalKoronaData.objects.get(pull_date = timezone.now())

    
    data_str = e.data.split(",")
    data = []
    for elem in data_str:
        data.append(int(elem))
    
    labels = e.bar_labels.split(',')
    print("labels splitted")
    d = MyBarChartDrawing(600, 350, (data, labels))
    print("Barchart called")
    binaryStuff = d.asString('jpeg')
    print("binarystuff done")
    return HttpResponse(binaryStuff, 'image/jpeg')
    
def testing(request):
    response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/processedThlData')
    textdata = response.json()
    cases = []
    barlabels = []
    i = 0
    for x in textdata['confirmed']['Kaikki sairaanhoitopiirit']:
        i = i + 1
        cases.append(x['value'])
        
    return render(request, 'ohsiha_app/test.html', {
        'cases': cases})

