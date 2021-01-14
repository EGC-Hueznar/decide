import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from base import mods
from base.tests import BaseTestCase
from .ldapMethods import LdapCensus
from .views import *


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

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

    #Comprueba si se crea una conexion con la base de datos
    def test_connection_check(self):
        connection = LdapCensus().ldapConnectionMethod('ldap.forumsys.com:389','cn=read-only-admin,dc=example,dc=com', 'password')
        self.assert_(connection is not None)


class ExportsFullCensusTest(BaseTestCase):
    def setUp(self):
        self.censusb = Census(voting_id=1, voter_id=1, type='VB')
        self.censusv = Census(voting_id=1, voter_id=1, type='V')
        self.censusb.save()
        self.censusv.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.censusb = None
        self.censusv = None

    def testFullExportDefault(self):
        response = self.client.get('/census/export/')
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.csv"')

    def testFullExportExcel(self):
        response = self.client.get('/census/export/?format=xls')
        self.assertEquals(response.get('Content-Type'), 'application/vnd.ms-excel')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.xls"')

    def testFullExportJson(self):
        response = self.client.get('/census/export/?format=json')
        self.assertEquals(response.get('Content-Type'), 'application/json')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.json"')

    def testFullExportFails(self):
        response = self.client.get('/census/export/?format=wrong_format')
        self.assertEquals(response.status_code, 400)


class ExportsCensusTest(BaseTestCase):
    def setUp(self):
        self.census = Census(voting_id=1, voter_id=1, type='VB')
        self.census.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def testFullExportDefault(self):
        response = self.client.get('/census/export/VB/1/')
        self.assertEquals(response.get('Content-Type'), 'text/csv')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.csv"')

    def testFullExportExcel(self):
        response = self.client.get('/census/export/VB/1/?format=xls')
        self.assertEquals(response.get('Content-Type'), 'application/vnd.ms-excel')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.xls"')

    def testFullExportJson(self):
        response = self.client.get('/census/export/VB/1/?format=json')
        self.assertEquals(response.get('Content-Type'), 'application/json')
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename="census.json"')

    def testFullExportFails(self):
        response = self.client.get('/census/export/VB/1/?format=wrong_format')
        self.assertEquals(response.status_code, 400)