from django.urls import path
from .views import BoothView
from django.views.generic import TemplateView


urlpatterns = [
    path('', BoothView.as_view()),
]
