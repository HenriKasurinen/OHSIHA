from django.db import models
from django.utils import timezone
import datetime

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart

import requests
import json

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):  
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)  

    def next_question(self):
        return self.pk + 1    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    category = models.IntegerField(default = 0)
    def __str__(self):
        return self.choice_text


class Ans(models.Model):
    respondent_name = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.IntegerField(default = 0)
    choise = models.ForeignKey(Choice, on_delete=models.CASCADE)
    date = models.DateField(default = timezone.now )
    def get_name (self):
        return self.respondent_name
    def get_question(self):
        return self.question.__str__
    def get_choise(self):
        return self.choise.__str__

class ExternalKoronaData(models.Model):
    pull_date = models.DateField(default = timezone.now )   
    data = models.TextField()
    bar_labels = models.TextField() 
    conf_amount = models.IntegerField(default=0)
    reco_amount = models.IntegerField(default=0)

    def pull_data_from_api(self):
        response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/processedThlData')
        textdata = response.json()
        cases = ""
        barlabels = ""
        i = 0
        a = 0
        for x in textdata['confirmed']['Kaikki sairaanhoitopiirit']:
            a = a + 1
            if(a>55):
                i = i + 1
                cases = cases + str(x['value']) + ','
                barlabels = barlabels + x['date'] + ","

        self.data = cases[:-1]
        self.bar_labels = barlabels[:-1] 
        self.last_pull_date = timezone.now()      

        response2 = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/v2')
        textdata2 = response2.json()
        self.conf_amount = len(textdata2['confirmed'])
        self.reco_amount = len(textdata2['recovered'])

    def give_data(self):
        return [self.data, self.bar_labels]

