# polls/urls.py
from django.urls import path
from . import views  

urlpatterns = [
    path("", views.index, name="index"),  # 👈 Cuando entras a /polls/, va a la vista index
]
