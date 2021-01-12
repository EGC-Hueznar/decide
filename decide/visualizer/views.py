import json
from django.views.generic import TemplateView, ListView
from django.conf import settings
from django.http import Http404
from base import mods
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from voting.models import *
import random

import telegram
import tweepy
from .telegrambot import *
from .twitterbot import *

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

        context["total"] = context["cantBin"] + context["cantPref"] + context["cantMult"] + context["cantNorm"] + context["cantidad"]
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
        elif(tipo == 'default'):
            self.template_name = "visualizer/listdefault.html"
            context['tipov'] = 'default'
            context['lista'] = Voting.objects.all()
        else:
            raise Http404
        return context

class VisualizerVista(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, tipo, voting_id, **kwargs):
        context = super().get_context_data(**kwargs)
        if(tipo == 'normal'):
            self.template_name = 'visualizer/resultnormal.html'
            context = self.normal(context, voting_id)
        elif(tipo == 'multiple'):
            self.template_name = 'visualizer/resultmul.html'
            context = self.multiple(context, voting_id)
        elif(tipo == 'preferencia'):
            self.template_name = 'visualizer/resultpref.html'
            context = self.preferencia(context, voting_id)
        elif(tipo == 'binaria'):
            self.template_name = 'visualizer/resultbin.html'
            context = self.binario(context, voting_id)
        else:
            raise Http404
        return context

    def normal(self, context, voting_id):
        votacion = Votacion.objects.get(id=voting_id)
        context['voting'] = votacion
        preguntas = Pregunta.objects.all().filter(votacion=votacion)
        context['resultados'] = preguntas
        respuestasMax = []
        respuestasMin = []
        respuestasMedia = []
        textos = []
        for pregunta in preguntas:
            textos.append(str(pregunta))
            respuestasMax.append(int(pregunta.Respuesta_Maxima()))
            respuestasMin.append(int(pregunta.Respuesta_Minima()))
            respuestasMedia.append(int(pregunta.Media_De_Las_Respuestas()))
        context['respuestasMax'] = respuestasMax
        context['respuestasMin'] = respuestasMin
        context['respuestasMedia'] = respuestasMedia
        context['textos'] = textos
        return context

    def multiple(self, context, voting_id):
        votacion = VotacionMultiple.objects.get(id=voting_id)
        context['voting'] = votacion
        pre = PreguntaMultiple.objects.all().filter(votacionMultiple=votacion)
        preguntas = {}
        for p in pre:
            opciones = OpcionMultiple.objects.all().filter(preguntaMultiple=p)
            preguntas[p] = opciones
        context['resultados'] = preguntas

        return context

    def preferencia(self, context, voting_id):
        votacion = VotacionPreferencia.objects.get(id=voting_id)
        context['voting'] = votacion
        pre = PreguntaPreferencia.objects.all().filter(votacionPreferencia=votacion)
        preguntas = {}
        for p in pre:
            opciones = OpcionRespuesta.objects.all().filter(preguntaPreferencia=p)
            preguntas[p] = opciones
        context['resultados'] = preguntas

        return context

    def binario(self, context, voting_id):
        votacion = VotacionBinaria.objects.get(id=voting_id)
        trues = (votacion.Numero_De_Trues())
        falses = (votacion.Numero_De_Falses())
        context['voting'] = votacion
        if ((trues + falses) != 0):
            context['porcentajesi'] = float("{:.4f}".format(trues/(trues + falses)))*100
            context['porcentajeno'] = float("{:.4f}".format(falses/(trues + falses)))*100
        else:
            context['porcentajesi'] = 0
            context['porcentajeno'] = 0
        return context


#======================================================================================


class VisualizerView(TemplateView):

    template_name = 'visualizer/visualizer.html'

    #funcion que devuelve diccionario con los objetos que se sumarán al context principal
    def grafica_votos(self, id):

        voting = get_object_or_404(Voting, pk=id)
        opcion = []
        voto = []
        puntuacion = []
        color = []
        
        i = 0 #esta variable nos servirá para definir las dimensiones de los ejes en la gráfica

        if(voting.postproc is not None):
            for item in voting.postproc:
                objeto = list(item.items())
                opcion.append(objeto[2][1]) #se coge el valor de la tupla (option, opcion x), que ocupa la posición 2 en la lista de tuplas
                voto.append(objeto[0][1]) #se hace lo mismo con la tupla (votos, x)
                puntuacion.append(objeto[3][1])
                #generamos el color que tendrá cada objeto en la gráfica de forma aleatoria
                r = lambda: random.randint(0,255)
                r = lambda: random.randint(0,255)
                color.append('#%02X%02X%02X' % (r(),r(),r()))
                i += 1
        #opcion = json.dumps(opcion)
        #voto = json.dumps(voto)
        #color = json.dumps(color)
        context = {
            'opcion':opcion,
            'voto':voto,
            'color':color,
            'puntuacion':puntuacion,
            'i':i
        }
        
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        context_grafica_votos = VisualizerView.grafica_votos(self, vid)
        
        try:
            r = mods.get('voting', params={'id': vid})
            #context['voting'] = json.dumps(r[0])
            voting = r[0]
            #context principal
            context = {
                'voting':voting
            }
            #hacer un update del context con los contexts de las funciones de las graficas
            context.update(context_grafica_votos)
            
        except:
            raise Http404

        return context


def telegram_report(self, **kwargs):
    voting_id = kwargs.get('voting_id', 0)
    r = mods.get('voting', params={'id': voting_id})
    voting = r[0]

    send_telegram_report_json(voting)

    return redirect('/visualizer/'+str(voting_id)+'/')

def twitter_report(self, **kwargs):
    voting_id = kwargs.get('voting_id', 0)
    r = mods.get('voting', params={'id': voting_id})
    voting = r[0]

    send_twitter_report_json(voting)

    return redirect('/visualizer/'+str(voting_id)+'/')
