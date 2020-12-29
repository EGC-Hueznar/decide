import json
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.http import Http404
#----------------------------------
import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from voting.models import Question, QuestionOption, Voting
from census.models import Census
from voting.serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
#----------------------------------------------------
from base import mods


class VisualizerList(ListView):
    template_name = 'visualizer/index.html'
    model = Voting


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
