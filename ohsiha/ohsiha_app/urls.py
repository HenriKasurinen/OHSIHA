from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

app_name = 'ohsiha_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('results', views.show_all_answers, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:user_id>/result_helper', views.result_helper, name = 'result_helper'),
    path('coach_home', views.coach_home, name = 'coach_home'),
    path('add_question', views.add_question, name = 'add_question'),
    path('delete_question', views.delete_question, name = 'delete_question'),
    path('modify_question', views.modify_question, name = 'modify_question'),
    path('rest_api/', views.ListDataView.as_view(), name="data-all")
]

