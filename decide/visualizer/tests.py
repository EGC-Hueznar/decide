from django.contrib.auth.models import User
from django.test import TestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question
import datetime
from census.models import Census


class VisualizerVotesTestCase(BaseTestCase):
    def setUp(self):
        q = Question(desc = "¿Te gusta?")
        q.save()
        self.v1=Voting(id=1, name="¿Te gusta EGC?", desc="Para saber si te gusta EGC", start_date=datetime.datetime(2020, 7, 6), question = q)
        self.v2=Voting(id=2, name="¿Te gusta PGPI?", desc="Para saber si te gusta PGPI", question = q)
        self.v3=Voting(id=3, name="¿Te gusta AII?", desc="Para saber si te gusta AII", start_date=datetime.datetime(2020, 10, 6), end_date=datetime.datetime(2021, 7, 6), question = q)
        self.v1.save()
        self.v2.save()
        self.v3.save()
        self.user = User(username='Daniel', is_staff=True)
        self.user.set_password('1234')
        self.user.save()
        self.c = Census(id=1, voting_id=1, voter_id = self.user.id)
        self.c.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v1=None
        self.v2=None
        self.v3=None
    def test_visualizer_index_page(self):
        self.login()
        response = self.client.get('/visualizer/', follow=True)
        self.assertEqual(response.status_code,200)
        v = Voting.objects.get(name = "¿Te gusta EGC?")
        self.assertEqual(v.desc, "Para saber si te gusta EGC")
    def test_visualizer_voting_results(self):
        self.login()
        response = self.client.get('/visualizer/{}'.format(self.v1.id), follow=True)
        self.assertEqual(response.status_code,200)
        v = Voting.objects.get(name = "¿Te gusta EGC?")
        self.assertEqual(v.desc, "Para saber si te gusta EGC")
