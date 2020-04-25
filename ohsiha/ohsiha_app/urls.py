from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = 'ohsiha_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('results', views.show_all_answers, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('chart', views.barchart, name='chart'),
    path('test', views.testing, name='test'),
    path('<int:user_id>/result_helper', views.result_helper, name = 'result_helper')
]

