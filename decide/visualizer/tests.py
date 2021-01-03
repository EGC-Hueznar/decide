from django.test import TestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question
import datetime
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
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v1=None
        self.v2=None
        self.v3=None
    def test_visualizer_index_page(self):
        self.login()
        response = self.client.get('/visualizer/')
        self.assertEqual(response.status_code,200)
        v = Voting.objects.get(name = "¿Te gusta EGC?")
        self.assertEqual(v.desc, "Para saber si te gusta EGC")
