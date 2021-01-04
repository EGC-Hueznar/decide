import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from base import mods
import telegram
from .telegrambot import *

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

def telegram_report(self, **kwargs):
    voting_id = kwargs.get('voting_id', 0)
    r = mods.get('voting', params={'id': voting_id})
    voting = r[0]
    
    send_telegram_report(voting)

    return redirect('/visualizer/'+str(voting_id)+'/')


   
