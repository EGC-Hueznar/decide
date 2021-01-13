from rest_framework.views import APIView
from rest_framework.response import Response
from voting.models import *
from django.http import HttpResponse
import json

def vistaBinaria(request,id):
    v =  VotacionBinaria.objects.filter(id=id).first().doPostProc()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def vistaBinariaAll(request):
    votaciones = VotacionBinaria.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.doPostProc()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

def vistaNormal(request,id):
    v =  Votacion.objects.filter(id=id).first().doPostProc()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def vistaNormalAll(request):
    votaciones = Votacion.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.doPostProc()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

def vistaMultiple(request,id):
    v =  VotacionMultiple.objects.filter(id=id).first().doPostProc()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def vistaMultipleAll(request):
    votaciones = VotacionMultiple.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.doPostProc()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')


def vistaPreferencia(request,id):
    v =  VotacionPreferencia.objects.filter(id=id).first().doPostProc()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def vistaPreferenciaAll(request):
    votaciones = VotacionPreferencia.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.doPostProc()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        return Response({})
