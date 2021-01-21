from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse

from base.perms import UserIsStaff
from .models import Census

from tablib import Dataset
from .resources import CensusResource
from .ldapMethods import LdapCensus
from django.contrib.auth.models import User
from voting.models import Voting
from django.db import models
from census.forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from voting.serializers import VotingSerializer


class CensusCreate(generics.ListCreateAPIView):

    def create(self, request, type, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter, type=type)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, type, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id, type=type).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)

        return Response('Valid voter')


class ListVotingsByVoter(generics.ListCreateAPIView):
    serializer_class = VotingSerializer

    def get(self, request, voter_id, *args, **kwargs):
        votaciones_binarias = [c.voting_id for c in Census.objects.filter(voter_id=voter_id) if c.type == 'VB']
        votaciones = [c.voting_id for c in Census.objects.filter(voter_id=voter_id) if c.type == 'V']
        votaciones_multiples = [c.voting_id for c in Census.objects.filter(voter_id=voter_id) if c.type == 'VM']
        votaciones_preferencia = [c.voting_id for c in Census.objects.filter(voter_id=voter_id) if c.type == 'VP']
        votings = [c.voting_id for c in Census.objects.filter(voter_id=voter_id) if c.type == 'Vo']
        return Response({'votaciones_binarias': votaciones_binarias,
                         'votaciones': votaciones,
                         'votaciones_multiples': votaciones_multiples,
                         'votaciones_preferencia': votaciones_preferencia,
                         'votings': votings})


def fullExport(request):
    census_resource = CensusResource()
    dataset = census_resource.export()
    if request.GET.get('format') == 'csv' or request.GET.get('format') is None:
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="census.csv"'
    elif request.GET.get('format') == 'xls':
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="census.xls"'
    elif request.GET.get('format') == 'json':
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="census.json"'
    else:
        response = HttpResponseBadRequest('Invalid format')
    return response


def export(request, type, voting_id):
    census_resourse = CensusResource()
    dataset = census_resourse.export(Census.objects.filter(voting_id=voting_id, type=type))
    if request.GET.get('format') == 'csv' or request.GET.get('format') is None:
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="census.csv"'
    elif request.GET.get('format') == 'xls':
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="census.xls"'
    elif request.GET.get('format') == 'json':
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="census.json"'
    else:
        response = HttpResponseBadRequest('Invalid format')
    return response


def importar(request):
    if request.method == 'POST':
        census_resource = CensusResource()
        dataset = Dataset()
        nuevos_censos = request.FILES['xlsfile']
        imported_data = dataset.load(nuevos_censos.read())
        result = census_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            census_resource.import_data(dataset, dry_run=False)  # Actually import now
    return render(request, 'importar.html')


# Este metodo procesa los parametros pasados por el formulario para llamar a los metodos de conexión e importación de LDAP para poder
# Crear así el censo con los usuarios de la rama de LDAP que se han pasado anteriormente, si y solo si esos usuarios estan registrados
# previamente en el sistema.
def importCensusFromLdapVotacion(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = CensusAddLdapFormVotacion(request.POST)

            if form.is_valid():
                urlLdap = form.cleaned_data['urlLdap']
                treeSufix = form.cleaned_data['treeSufix']
                pwd = form.cleaned_data['pwd']
                branch = form.cleaned_data['branch']
                voting = form.cleaned_data['voting'].__getattribute__('pk')

                voters = User.objects.all()
                usernameList = LdapCensus().LdapGroups(urlLdap, treeSufix, pwd, branch)

                userList = []
                for username in usernameList:

                    user = voters.filter(username=username)
                    if user:
                        user = user.values('id')[0]['id']
                        userList.append(user)

            if request.user.is_authenticated:
                for username in userList:
                    census = Census(voting_id=voting, voter_id=username, type='Vo')
                    census.save()

            return redirect('/admin/census/census')
        else:
            form = CensusAddLdapFormVotacion()

        context = {
            'form': form,
        }
        return render(request, template_name='importarCensusLdapVotacion.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, "permiso denegado")
        return redirect('/admin')


def main_census(request):
    census = Census.objects.all()
    votings = Voting.objects.all()
    voters = User.objects.all()
    return render(request, "main_index.html", {'census': census, 'votings': votings, 'voters': voters})


# Este metodo procesa los parametros pasados por el formulario para llamar a los metodos de conexión e importación de LDAP para poder
# Crear así el censo con los usuarios de la rama de LDAP que se han pasado anteriormente, si y solo si esos usuarios estan registrados
# previamente en el sistema.
def importCensusFromLdapBinaria(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = CensusAddLdapFormVotacionBinaria(request.POST)

            if form.is_valid():

                urlLdap = form.cleaned_data['urlLdap']
                treeSufix = form.cleaned_data['treeSufix']
                pwd = form.cleaned_data['pwd']
                branch = form.cleaned_data['branch']
                voting = form.cleaned_data['voting'].__getattribute__('pk')

                voters = User.objects.all()
                usernameList = LdapCensus().LdapGroups(urlLdap, treeSufix, pwd, branch)

                userList = []
                for username in usernameList:

                    user = voters.filter(username=username)
                    if user:
                        user = user.values('id')[0]['id']
                        userList.append(user)

                if request.user.is_authenticated:
                    for username in userList:
                        # census = Census(voting_id=voting, voter_id=username)
                        census = Census(voting_id=voting, voter_id=username, type='VB')
                        census.save()

            return redirect('/admin/census/census')
        else:

            form = CensusAddLdapFormVotacionBinaria()

        context = {
            'form': form,
        }
        return render(request, template_name='importarCensusLdapBinaria.html', context=context)

    else:
        messages.add_message(request, messages.ERROR, "permiso denegado")
        return redirect('/admin')


# Este metodo procesa los parametros pasados por el formulario para llamar a los metodos de conexión e importación de LDAP para poder
# Crear así el censo con los usuarios de la rama de LDAP que se han pasado anteriormente, si y solo si esos usuarios estan registrados
# previamente en el sistema.
def importCensusFromLdapMultiple(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = CensusAddLdapFormVotacionMultiple(request.POST)

            if form.is_valid():
                urlLdap = form.cleaned_data['urlLdap']
                treeSufix = form.cleaned_data['treeSufix']
                pwd = form.cleaned_data['pwd']
                branch = form.cleaned_data['branch']
                voting = form.cleaned_data['voting'].__getattribute__('pk')

                voters = User.objects.all()
                usernameList = LdapCensus().LdapGroups(urlLdap, treeSufix, pwd, branch)

                userList = []
                for username in usernameList:

                    user = voters.filter(username=username)
                    if user:
                        user = user.values('id')[0]['id']
                        userList.append(user)

            if request.user.is_authenticated:
                for username in userList:
                    census = Census(voting_id=voting, voter_id=username, type='VM')
                    census.save()

            return redirect('/admin/census/census')
        else:
            form = CensusAddLdapFormVotacionMultiple()

        context = {
            'form': form,
        }
        return render(request, template_name='importarCensusLdapMultiple.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, "permiso denegado")
        return redirect('/admin')


# Este metodo procesa los parametros pasados por el formulario para llamar a los metodos de conexión e importación de LDAP para poder
# Crear así el censo con los usuarios de la rama de LDAP que se han pasado anteriormente, si y solo si esos usuarios estan registrados
# previamente en el sistema.
def importCensusFromLdapPreferencia(request):
    if request.user.is_staff:

        if request.method == 'POST':
            form = CensusAddLdapFormVotacionPreferencia(request.POST)

            if form.is_valid():
                urlLdap = form.cleaned_data['urlLdap']
                treeSufix = form.cleaned_data['treeSufix']
                pwd = form.cleaned_data['pwd']
                branch = form.cleaned_data['branch']
                voting = form.cleaned_data['voting'].__getattribute__('pk')

                voters = User.objects.all()
                usernameList = LdapCensus().LdapGroups(urlLdap, treeSufix, pwd, branch)

                userList = []
                for username in usernameList:

                    user = voters.filter(username=username)
                    if user:
                        user = user.values('id')[0]['id']
                        userList.append(user)

            if request.user.is_authenticated:
                for username in userList:
                    census = Census(voting_id=voting, voter_id=username, type='VP')

                    census.save()

            return redirect('/admin/census/census')
        else:
            form = CensusAddLdapFormVotacionPreferencia()

        context = {
            'form': form,
        }
        return render(request, template_name='importarCensusLdapPreferencia.html', context=context)
    else:
        messages.add_message(request, messages.ERROR, "permiso denegado")
        return redirect('/admin')


def clone(request, type, voting_id):
    target_id = request.GET.get('target_id')
    target_type = request.GET.get('target_type')

    if target_id is None or target_type is None:
        return HttpResponseBadRequest('Target id and type are required.')

    voters_to_clone = [c.voter_id for c in Census.objects.filter(type=type, voting_id=voting_id)]
    current_voters = [c.voter_id for c in Census.objects.filter(type=target_type, voting_id=target_id)]
    added_voters = []
    for voter_id in voters_to_clone:
        if voter_id not in current_voters:
            c = Census(type=target_type, voting_id=target_id, voter_id=voter_id)
            c.save()
            added_voters.append(voter_id)
    return JsonResponse({'target_id': target_id,
                         'target_type': target_type,
                         'voters_cloned': added_voters})
