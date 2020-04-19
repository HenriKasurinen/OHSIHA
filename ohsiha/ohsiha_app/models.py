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
    def __str__(self):
        return self.choice_text


class Ans(models.Model):
    respondent_name = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise = models.ForeignKey(Choice, on_delete=models.CASCADE)
    def get_name (self):
        return self.respondent_name
    def get_question(self):
        return self.question.__str__
    def get_choise(self):
        return self.choise.__str__

class MyBarChartDrawing(models.Model, Drawing):
    def __init__(self, width=600, height=350, *args, **kw):
        response = requests.get('https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/processedThlData')
        textdata = response.json()
        cases = []
        barlabels = []
        i = 0
        a = 0
        for x in textdata['confirmed']['Kaikki sairaanhoitopiirit']:
            a = a + 1
            if(a>55):
                i = i + 1
                cases.append(x['value'])
                if i == 10:
                    barlabels.append(x['date'][8:10] + "." + x['date'][5:7])
                    i = 0
                else:
                    barlabels.append(" ")    
            

        Drawing.__init__(self,width,height,*args,**kw)
        self.add(VerticalBarChart(), name='chart')

        #set any shapes, fonts, colors you want here.  We'll just
        #set a title font and place the chart within the drawing
        self.chart.x = 20
        self.chart.y = 15
        self.chart.width = self.width - 10
        self.chart.height = self.height - 10

        self.chart.data = [cases]

        self.chart.valueAxis.valueMin = min(cases)
        self.chart.valueAxis.valueMax = max(cases) + 2
        self.chart.valueAxis.labels.fontName = 'Helvetica'
        self.chart.valueAxis.labels.fontSize = 10
        self.chart.valueAxis.labelTextFormat = '%0.0f'
        self.chart.valueAxis.labels.dx = -5

        self.chart.categoryAxis.labels.boxAnchor = 'c'
        self.chart.categoryAxis.labels.fontName = 'Helvetica'
        self.chart.categoryAxis.labels.fontSize = 12
        self.chart.categoryAxis.tickDown = 0
        self.chart.categoryAxis.labels.dx = 0
        self.chart.categoryAxis.labels.dy = -7
        self.chart.categoryAxis.labels.angle = 0
        self.chart.categoryAxis.categoryNames = barlabels

    