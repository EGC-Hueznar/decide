import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census

from base import mods
from base.tests import BaseTestCase
from .ldapMethods import LdapCensus
from .views import *
from datetime import datetime
import pytz
import time


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()
        self.vb = VotacionBinaria(titulo='titulo 1', descripcion='Descripcion1', fecha_inicio=datetime(2021,1,15,9,00, tzinfo=pytz.UTC), fecha_fin=datetime(2021,1,16,9,00, tzinfo=pytz.UTC))
        self.vm = VotacionMultiple(titulo='titulo 1', descripcion='Descripcion1', fecha_inicio=datetime(2021,1,15,9,00, tzinfo=pytz.UTC), fecha_fin=datetime(2021,1,16,9,00, tzinfo=pytz.UTC))
        self.vo = Votacion(titulo='titulo 1', descripcion='Descripcion1', fecha_inicio=datetime(2021,1,15,9,00, tzinfo=pytz.UTC), fecha_fin=datetime(2021,1,16,9,00, tzinfo=pytz.UTC))
        self.vp = VotacionPreferencia(titulo='titulo 1', descripcion='Descripcion1', fecha_inicio=datetime(2021,1,15,9,00, tzinfo=pytz.UTC), fecha_fin=datetime(2021,1,16,9,00, tzinfo=pytz.UTC))
        self.vb.save()
        self.vm.save()
        self.vo.save()
        self.vp.save()
    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())

    #Añade censo a una votación binaria que tenga fechas de inicio y fin distintas a null
    #El usuario que añadirá el censo será administrador del sistema
    def test_ldap_check_votacion_preferencia_pass(self):
        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        votacion = VotacionPreferencia.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusPreferencia/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes+1,despues)
    
    def test_ldap_check_votacion_preferencia_get(self):
        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
    
        self.client.force_login(admin)
        votacion = VotacionPreferencia.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        response = self.client.get('/census/addLDAPcensusPreferencia/')
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(antes,despues)
    
    def test_ldap_check_votacion_preferencia_wrongLogin(self):

        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(u)
        votacion = VotacionPreferencia.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusPreferencia/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes,despues)
   
    def test_ldap_check_votacion_binaria_pass(self):
        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        votacion = VotacionBinaria.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusBinaria/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes+1,despues)

    def test_ldap_check_votacion_binaria_get(self):
        antes = Census.objects.count()
      
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        votacion = VotacionBinaria.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        response = self.client.get('/census/addLDAPcensusBinaria/')
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(antes,despues)

    #Añade censo a una votación binaria que tenga fechas de inicio y fin distintas a null
    #El usuario que añadirá el censo no será administrador del sistema y por lo tanto se espera que no se añada censo
    def test_ldap_check_votacion_binaria_wrong_login(self):


        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(u)
        votacion = VotacionBinaria.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        self.client.post('/census/addLDAPcensusBinaria/', data)
        despues = Census.objects.count()
        self.assertEqual(antes,despues)

    #Añade censo a una votación multiple que tenga fechas de inicio y fin distintas a null
    #El usuario que añadirá el censo será administrador del sistema
    def test_ldap_check_votacion_Multiple_pass(self):


        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        votacion = VotacionMultiple.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusMultiple/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes+1,despues)

    #Añade censo a una votación multiple que tenga fechas de inicio y fin distintas a null
    #El usuario que añadirá el censo no será administrador del sistema y por lo tanto se espera que no se añada censo
    def test_ldap_check_votacion_Multiple_wrong_login(self):


        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(u)
        votacion = VotacionMultiple.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        self.client.post('/census/addLDAPcensusMultiple/', data)
        despues = Census.objects.count()
        self.assertEqual(antes,despues)

    def test_ldap_check_votacion_multiple_get(self):
        antes = Census.objects.count()
      
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        response = self.client.get('/census/addLDAPcensusMultiple/')
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(antes,despues)
    
    def test_ldap_check_votacion_pass(self):

        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        votacion = Votacion.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusVotacion/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes+1,despues)

    def test_ldap_check_votacion_wrong_login(self):

        antes = Census.objects.count()
        #Guardamos al usuario a introducir que ya esta en el ldap
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(u)
        votacion = Votacion.objects.all().filter(fecha_inicio__isnull=False, fecha_fin__isnull=False)[0].id
        data = {'voting': votacion, 'urlLdap': 'ldap.forumsys.com:389', 'branch': 'ou=chemists,dc=example,dc=com', 'treeSufix': 'cn=read-only-admin,dc=example,dc=com','pwd': 'password'}
        response = self.client.post('/census/addLDAPcensusVotacion/', data)
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(antes,despues)


    
    def test_ldap_check_votacion_get(self):
        antes = Census.objects.count()
      
        u = User(username='curie')
        u.set_password('123')
        u.save()

        admin = User(username='administrado')
        admin.set_password('1234567asd')
        admin.is_staff = True
        admin.save()

        #Hacemos la request
        
        self.client.force_login(admin)
        response = self.client.get('/census/addLDAPcensusVotacion/')
        despues = Census.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(antes,despues)
    