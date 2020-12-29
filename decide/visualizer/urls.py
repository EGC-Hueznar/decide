from django.urls import path
from .views import VisualizerView, VisualizerList


urlpatterns = [
    path('', VisualizerList.as_view(), name='visualizer'),
    path('<int:voting_id>/', VisualizerView.as_view()),
]
