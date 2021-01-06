from django.contrib.auth.models import User
from django.test import TestCase
from base.tests import BaseTestCase
from voting.models import Voting, Question, Votacion, VotacionBinaria, VotacionPreferencia, VotacionMultiple
import datetime
from census.models import Census


class VisualizerVotesTestCase(BaseTestCase):
    def setUp(self):
        q = Question(desc = "Aquí tiene su pregunta: ")
        q.save()

        self.vo1=Votacion(id=1, titulo="¿Te gusta EGC?", fecha_inicio=datetime.datetime(2020, 7, 6))
        self.vo2=Votacion(id=2, titulo="¿Te gusta PGPI?")
        self.vo3=Votacion(id=3, titulo="¿Te gusta AII?", fecha_inicio=datetime.datetime(2020, 10, 6), fecha_fin=datetime.datetime(2021, 7, 6))

        self.vp1=VotacionPreferencia(id=1, titulo="¿Te gusta EGC?", fecha_inicio=datetime.datetime(2020, 7, 6))
        self.vp2=VotacionPreferencia(id=2, titulo="¿Te gusta PGPI?")
        self.vp3=VotacionPreferencia(id=3, titulo="¿Te gusta AII?", fecha_inicio=datetime.datetime(2020, 10, 6), fecha_fin=datetime.datetime(2021, 7, 6))

        self.vm1=VotacionMultiple(id=1, titulo="¿Te gusta EGC?", fecha_inicio=datetime.datetime(2020, 7, 6))
        self.vm2=VotacionMultiple(id=2, titulo="¿Te gusta PGPI?")
        self.vm3=VotacionMultiple(id=3, titulo="¿Te gusta AII?", fecha_inicio=datetime.datetime(2020, 10, 6), fecha_fin=datetime.datetime(2021, 7, 6))

        self.vb1=VotacionBinaria(id=1, titulo="¿Te gusta EGC?", fecha_inicio=datetime.datetime(2020, 7, 6))
        self.vb2=VotacionBinaria(id=2, titulo="¿Te gusta PGPI?")
        self.vb3=VotacionBinaria(id=3, titulo="¿Te gusta AII?", fecha_inicio=datetime.datetime(2020, 10, 6), fecha_fin=datetime.datetime(2021, 7, 6))

        self.v1=Voting(id=1, name="¿Te gusta EGC?", start_date=datetime.datetime(2020, 7, 6), question = q)
        self.v2=Voting(id=2, name="¿Te gusta PGPI?", question = q)
        self.v3=Voting(id=3, name="¿Te gusta AII?", start_date=datetime.datetime(2020, 10, 6), end_date=datetime.datetime(2021, 7, 6), question = q)

        self.vo1.save()
        self.vo2.save()
        self.vo3.save()

        self.vp1.save()
        self.vp2.save()
        self.vp3.save()

        self.vm1.save()
        self.vm2.save()
        self.vm3.save()

        self.vb1.save()
        self.vb2.save()
        self.vb3.save()

        self.v1.save()
        self.v2.save()
        self.v3.save()
        self.c = Census(id=1, voting_id=1, voter_id = 1)
        self.c.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.c=None
        self.user=None

        self.vo1=None
        self.vo2=None
        self.vo3=None

        self.vp1=None
        self.vp2=None
        self.vp3=None

        self.vm1=None
        self.vm2=None
        self.vm3=None

        self.vb1=None
        self.vb2=None
        self.vb3=None

        self.v1=None
        self.v2=None
        self.v3=None
    def test_visualizer_index_page(self):
        self.login()
        response = self.client.get('/visualizer/', follow=True)
        self.assertEqual(response.status_code,200)
        vo1 = Votacion.objects.get(titulo = "¿Te gusta EGC?")
        self.assertEqual(vo1.titulo, "¿Te gusta EGC?")
    def test_visualizer_normal(self):
        self.login()
        response = self.client.get('/visualizer/normal', follow=True)
        self.assertEqual(response.status_code,200)
        response = self.client.get('/visualizer/normal/{}'.format(self.vo1.id), follow=True)
        self.assertEqual(response.status_code,200)
        vo1 = Votacion.objects.get(titulo = "¿Te gusta EGC?")
        self.assertEqual(vo1.titulo, "¿Te gusta EGC?")
