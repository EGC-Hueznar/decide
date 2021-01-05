from django.urls import path
from .views import *



urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/telegram_report', telegram_report),
    path('<int:voting_id>/twitter_report', twitter_report),
]
