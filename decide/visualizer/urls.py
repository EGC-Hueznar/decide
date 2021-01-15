from django.urls import path
from .views import *



urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('voting/<int:voting_id>/', VisualizerView.as_view()),
    path('', VisualizerIndex.as_view()),
    path('<str:tipo>/', VisualizerVotingList.as_view()),
    path('<str:tipo>/<int:voting_id>/', VisualizerVista.as_view()),
    path('<int:voting_id>/telegram_report', telegram_report),
    path('<str:tipo>/<int:voting_id>/telegram_report', telegram_report),
    path('<int:voting_id>/twitter_report', twitter_report),
    path('<str:tipo>/<int:voting_id>/twitter_report', twitter_report),
]
