import json
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.http import Http404
from voting.models import Voting#, VotacionBinaria, Votacion, VotacionMultiple, VotacionPreferencia
from base import mods
from django.shortcuts import render

class VisualizerIndex(TemplateView):
    template_name = 'visualizer/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantNorm'] = Voting.objects.count()#Votacion.objects.count()
        context['cantNProx'] = Voting.objects.filter(start_date__isnull=True).count()#Votacion.objects.filter(start_date__isnull=True).count()
        context['cantNFin'] = Voting.objects.filter(end_date__isnull=False).count()#Votacion.objects.filter(end_date__isnull=False).count()
        context['cantNPend'] = context['cantNorm'] - context['cantNProx'] - context['cantNFin']

        context['cantPref'] = Voting.objects.count()#VotacionPreferencia.objects.count()
        context['cantPProx'] = Voting.objects.filter(start_date__isnull=True).count()#VotacionPreferencia.objects.filter(start_date__isnull=True).count()
        context['cantPFin'] = Voting.objects.filter(end_date__isnull=False).count()#VotacionPreferencia.objects.filter(end_date__isnull=False).count()
        context['cantPPend'] = context['cantPref']  - context['cantPProx'] - context['cantPFin']

        context['cantMult'] = Voting.objects.count()#VotacionMultiple.objects.count()
        context['cantMProx'] = Voting.objects.filter(start_date__isnull=True).count()#VotacionMultiple.objects.filter(start_date__isnull=True).count()
        context['cantMFin'] = Voting.objects.filter(end_date__isnull=False).count()#VotacionMultiple.objects.filter(end_date__isnull=False).count()
        context['cantMPend'] = context['cantMult'] - context['cantMProx'] - context['cantMFin']

        context['cantBin'] = Voting.objects.count()#VotacionBinaria.objects.count()
        context['cantBProx'] = Voting.objects.filter(start_date__isnull=True).count()#VotacionBinaria.objects.filter(start_date__isnull=True).count()
        context['cantBFin'] = Voting.objects.filter(end_date__isnull=False).count()#VotacionBinaria.objects.filter(end_date__isnull=False).count()
        context['cantBPend'] = context['cantBin'] - context['cantBProx'] - context['cantBFin']
        return context

class VisualizerVotingList(TemplateView):
    template_name = 'visualizer/list.html'

    def get_context_data(self,tipo,**kwargs):
        context = super().get_context_data(**kwargs)
        if(tipo == 'normal'):
            context['tipov'] = 'normal'
            context['lista'] = Voting.objects.all() #Votacion.objects.all()
        elif(tipo == 'multiple'):
            context['tipov'] = 'lista'
            context['lista'] = Voting.objects.all() #VotacionMultiple.objects.all()
        elif(tipo == 'preferencia'):
            context['tipov'] = 'preferencia'
            context['lista'] = Voting.objects.all() #VotacionPreferencia.objects.all()
        elif(tipo == 'binaria'):
            context['tipov'] = 'binaria'
            context['lista'] = Voting.objects.all() #VotacionBinaria.objects.all()
        else:
            raise Http404
        return context

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
