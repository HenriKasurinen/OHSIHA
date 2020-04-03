from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice, Input, MyBarChartDrawing
from django.views  import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
import requests
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
    model = Question
    template_name = 'ohsiha_app/results.html'
    permission_denied_message = "You are not allowed here."


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
        response = Input()
        response.respondent_name = request.user
        response.qestion = question
        response.choise = selected_choice
        response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ohsiha_app:results', args=(question.id,)))

def home(request):
    response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/v2')
    textdata = response.json()
    conf_amount = len(textdata['confirmed'])
    reco_amount = len(textdata['recovered'])
    
    return render(request, 'ohsiha_app/home.html', {
        'confirmed':  conf_amount,
        'recovered':  reco_amount
    })

@login_required
def barchart(request):

    #instantiate a drawing object
    d = MyBarChartDrawing()
    binaryStuff = d.asString('jpeg')
    return HttpResponse(binaryStuff, 'image/jpeg')
    