import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from voting.models import *
from django.http import HttpResponse
import json
from django.core import serializers

def votacionBinariaATxt(id):
    v = VotacionBinaria.objects.filter(id=id).first()
    res = "Titulo: " + v.titulo + "\n" + \
          "Descripcion: " + v.descripcion+"\n"+\
          "Fecha de Inicio de la Votación: "+ str(v.fecha_inicio)+"\n"+\
           "Fecha de Fin de la Votación: " + str(v.fecha_fin)+"\n"+\
            "Número de Respuestas a Sí: " + str(v.Numero_De_Trues())+"\n"+ \
          "Número de Respuestas a No: " + str(v.Numero_De_Falses())+"\n";
    return res;
def downloadVotacionBinaria(request,id):
    res = votacionBinariaATxt(id)
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Binaria.txt"'
    return response

def downloadAllVotacionBinaria(request):
    votaciones = VotacionBinaria.objects.all()
    res = ""
    for v in votaciones:
        res = res +  votacionBinariaATxt(v.id)
        res = res + "-------------------------------\n"
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Binaria Todas.txt"'
    return response

def  getVotacionBinariaById(request,id):
    v = VotacionBinaria.objects.filter(id=id).first().toJson()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def getAllVotacionesBinarias(request):
    votaciones = VotacionBinaria.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.toJson()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

#-----------------------------------------------------

def votacionNormalATxt(id):
    v = Votacion.objects.filter(id=id).first()
    res = "Titulo: " + v.titulo + "\n" + \
          "Descripcion: " + v.descripcion+"\n"+\
          "Fecha de Inicio de la Votación: "+ str(v.fecha_inicio)+"\n"+\
          "Fecha de Fin de la Votación: " + str(v.fecha_fin)+"\n"+\
           "Número de preguntas: " +  str(v.Numero_De_Preguntas())+"\n"+\
           "Preguntas de la votación: "+"\n"+\
            "*************************"+"\n"

    for pregunta in v.preguntas.all():
        res = res + " -Pregunta: "+ pregunta.textoPregunta+"\n" +\
                "Número de respuestas: "+ str(pregunta.Numero_De_Respuestas())+"\n"+\
                "Media de las respuestas: "+ str(pregunta.Media_De_Las_Respuestas())+"\n"+\
                "Respuesta máxima: "+ str(pregunta.Respuesta_Maxima())+"\n"+\
                "Respuesta mínima: "+ str(pregunta.Respuesta_Minima())+"\n"
    return res

def downloadVotacionNomral(request,id):
    res = votacionNormalATxt(id)
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Normal.txt"'
    return response

def downloadAllVotacionNormal(request):
    votaciones = Votacion.objects.all()
    res = ""
    for v in votaciones:
        res = res +  votacionNormalATxt(v.id)
        res = res + "-------------------------------\n"
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Normal Todas.txt"'
    return response

def  getVotacionById(request,id):
    v = Votacion.objects.filter(id=id).first().toJson()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def getAllVotaciones(request):
    votaciones = Votacion.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.toJson()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

#-----------------------------------------------------

def votacionMultipleATxt(id):
    v = VotacionMultiple.objects.filter(id=id).first()
    res = "Titulo: " + v.titulo + "\n" + \
          "Descripcion: " + v.descripcion+"\n"+\
          "Fecha de Inicio de la Votación: "+ str(v.fecha_inicio)+"\n"+\
          "Fecha de Fin de la Votación: " + str(v.fecha_fin)+"\n"+\
           "Número de preguntas: " +  str(v.Numero_De_Preguntas_Multiple())+"\n"+\
           "Preguntas de la votación: "+"\n"+\
            "*************************"+"\n"

    for pregunta in v.preguntasMultiples.all():
        res = res + " -Pregunta: "+ pregunta.textoPregunta+"\n" +\
                "Número de opciones: "+ str(pregunta.Numero_De_Opciones())+"\n"+\
                "Votos dados a las opciones: "+ str(pregunta.cuentaOpcionesMultiple())+"\n"
    return res

def downloadVotacionMultiple(request,id):
    res = votacionMultipleATxt(id)
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Multiple.txt"'
    return response

def downloadAllVotacionMultiple(request):
    votaciones = VotacionMultiple.objects.all()
    res = ""
    for v in votaciones:
        res = res +  votacionMultipleATxt(v.id)
        res = res + "-------------------------------\n"
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Multiple Todas.txt"'
    return response

def  getVotacionMultipleById(request,id):
    v = VotacionMultiple.objects.filter(id=id).first().toJson()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def getAllVotacionesMultiples(request):
    votaciones = VotacionMultiple.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.toJson()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')

#-----------------------------------------------------

def votacionPreferenciaATxt(id):
    v = VotacionPreferencia.objects.filter(id=id).first()
    res = "Titulo: " + v.titulo + "\n" + \
          "Descripcion: " + v.descripcion+"\n"+\
          "Fecha de Inicio de la Votación: "+ str(v.fecha_inicio)+"\n"+\
          "Fecha de Fin de la Votación: " + str(v.fecha_fin)+"\n"+\
           "Número de preguntas: " +  str(v.Numero_De_Preguntas_Preferencia())+"\n"+\
           "Preguntas de la votación: "+"\n"+\
            "*************************"+"\n"

    for pregunta in v.preguntasPreferencia.all():
        res = res + " -Pregunta: "+ pregunta.textoPregunta+"\n" +\
                "Número de opciones: "+ str(pregunta.Numero_De_Opciones())+"\n"+\
                "Opciones de la Pregunta: \n"
        for opcion in pregunta.opcionesRespuesta.all():
            res  = res + "Opción: "+ opcion.nombre_opcion+"\n"+\
                "Media de Preferencia de la opción: "+str(opcion.Media_Preferencia())+"\n"+\
                "Respuestas de la opción: " + str(opcion.Respuestas_Opcion())+"\n"

    return res

def downloadVotacionPreferencia(request,id):
    res = votacionPreferenciaATxt(id)
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Preferencia.txt"'
    return response

def downloadAllVotacionPreferencia(request):
    votaciones = VotacionPreferencia.objects.all()
    res = ""
    for v in votaciones:
        res = res +  votacionPreferenciaATxt(v.id)
        res = res + "-------------------------------\n"
    response = HttpResponse(res, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Votacion Preferencia Todas.txt"'
    return response

def  getVotacionPreferenciaById(request,id):
    v = VotacionPreferencia.objects.filter(id=id).first().toJson()
    v = json.dumps(v)
    return HttpResponse(v, content_type='application/json')

def getAllVotacionesPreferencia(request):
    votaciones = VotacionPreferencia.objects.all()
    res = {}
    listaVotaciones = []
    for v in votaciones:
        js = v.toJson()
        listaVotaciones.append(js)
    res['votaciones'] = listaVotaciones
    res = json.dumps(res)
    return HttpResponse(res, content_type='application/json')


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def get(self, request, *args, **kwargs):
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)