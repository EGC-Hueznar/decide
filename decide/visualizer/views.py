import json
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.http import Http404
from voting.models import Voting, VotacionBinaria, Votacion, VotacionMultiple, VotacionPreferencia
from base import mods
from django.shortcuts import render

class VisualizerIndex(TemplateView):
    template_name = 'visualizer/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cantNorm'] = Votacion.objects.count()
        context['cantNProx'] = Votacion.objects.filter(fecha_inicio__isnull=True).count()
        context['cantNFin'] = Votacion.objects.filter(fecha_fin__isnull=False).count()
        context['cantNPend'] = context['cantNorm'] - context['cantNProx'] - context['cantNFin']

        context['cantPref'] = VotacionPreferencia.objects.count()
        context['cantPProx'] = VotacionPreferencia.objects.filter(fecha_inicio__isnull=True).count()
        context['cantPFin'] = VotacionPreferencia.objects.filter(fecha_fin__isnull=False).count()
        context['cantPPend'] = context['cantPref']  - context['cantPProx'] - context['cantPFin']

        context['cantMult'] = VotacionMultiple.objects.count()
        context['cantMProx'] = VotacionMultiple.objects.filter(fecha_inicio__isnull=True).count()
        context['cantMFin'] = VotacionMultiple.objects.filter(fecha_fin__isnull=False).count()
        context['cantMPend'] = context['cantMult'] - context['cantMProx'] - context['cantMFin']

        context['cantBin'] = VotacionBinaria.objects.count()
        context['cantBProx'] = VotacionBinaria.objects.filter(fecha_inicio__isnull=True).count()
        context['cantBFin'] = VotacionBinaria.objects.filter(fecha_fin__isnull=False).count()
        context['cantBPend'] = context['cantBin'] - context['cantBProx'] - context['cantBFin']

        context['cantidad'] = Voting.objects.count()
        context['cantProx'] = Voting.objects.filter(start_date__isnull=True).count()
        context['cantFin'] = Voting.objects.filter(end_date__isnull=False).count()
        context['cantPend'] = context['cantidad'] - context['cantProx'] - context['cantFin']

        context["total"] = context["cantBin"] + context["cantPref"] + context["cantMult"] + context["cantNorm"]
        return context

class VisualizerVotingList(TemplateView):
    template_name = 'visualizer/list.html'

    def get_context_data(self,tipo,**kwargs):
        context = super().get_context_data(**kwargs)
        if(tipo == 'normal'):
            context['tipov'] = 'normal'
            context['lista'] = Votacion.objects.all()
        elif(tipo == 'multiple'):
            context['tipov'] = 'lista'
            context['lista'] = VotacionMultiple.objects.all()
        elif(tipo == 'preferencia'):
            context['tipov'] = 'preferencia'
            context['lista'] = VotacionPreferencia.objects.all()
        elif(tipo == 'binaria'):
            context['tipov'] = 'binaria'
            context['lista'] = VotacionBinaria.objects.all()
        else:
            context['tipov'] = 'default'
            context['lista'] = Voting.objects.all()
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
