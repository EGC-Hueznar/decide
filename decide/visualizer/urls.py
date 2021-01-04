from django.urls import path
from .views import *



urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/<telegram>', send_telegram_report),
]
