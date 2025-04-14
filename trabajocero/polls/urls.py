from django.urls import path
from . import views

app_name = "polls"  # esto es importante para usar {% url 'polls:detail' %}

urlpatterns = [
    path("", views.index, name="index"),  # /polls/
    path("<int:question_id>/", views.detail, name="detail"),  # /polls/34/
    path("<int:question_id>/results/", views.results, name="results"),  # /polls/34/results/
    path("<int:question_id>/vote/", views.vote, name="vote"),  # /polls/34/vote/
]
