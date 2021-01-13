# Generated by Selenium IDE
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

from voting.models import Voting, Question, VotacionBinaria, VotacionPreferencia, VotacionMultiple, Votacion

from census.models import Census
class TestVisualizerIndex(StaticLiveServerTestCase):
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
        self.user = User(id = 1, username='Daniel', is_staff=True)
        self.user.set_password('1234')
        self.user.save()
        self.c = Census(id=1, voting_id=1, voter_id = 1)
        self.c.save()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
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
    def test_visualizerIndexNormal(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_link_text("Ver").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/normal/".format(self.live_server_url))
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vo1.titulo).click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/normal/{}/".format(self.live_server_url, self.vo1.id))

    def test_visualizerIndexPref(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_css_selector("tr:nth-child(2) .btn").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/preferencia/".format(self.live_server_url))
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vp2.titulo).click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/preferencia/{}/".format(self.live_server_url, self.vp2.id))

    def test_visualizerIndexMult(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_css_selector("tr:nth-child(3) .btn").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/multiple/".format(self.live_server_url))
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vm3.titulo).click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/multiple/{}/".format(self.live_server_url, self.vm3.id))

    def test_visualizerIndexBin(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_css_selector("tr:nth-child(4) .btn").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/binaria/".format(self.live_server_url))
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vb2.titulo).click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/binaria/{}/".format(self.live_server_url, self.vb2.id))

class TestGraficasVotacionNormal(StaticLiveServerTestCase):
    def setUp(self):
        q = Question(desc = "Aquí tiene su pregunta: ")
        q.save()

        self.vo1=Votacion(id=1, titulo="Viva el Sevilla", fecha_inicio=datetime.datetime(2020, 7, 6), fecha_fin=datetime.datetime(2021, 7, 6))
        
        self.vo1.save()

        self.user = User(id = 1, username='Manuel', is_staff=True)
        self.user.set_password('contraseña')
        self.user.save()
        self.c = Census(id=1, voting_id=1, voter_id = 1)
        self.c.save()

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
  
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.c=None
        self.user=None

        self.vo1=None

    def test_mostrar_grafico_sectores(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        self.driver.find_element(By.LINK_TEXT, "Ver").click()
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vo1.titulo).click()
        time.sleep(3)
        self.driver.find_element(By.ID, "enseñarTarta").click()
        time.sleep(3)
        self.assertEqual(self.driver.find_element(By.ID, "graficabarras").get_attribute("style"), "display: none;")

    def test_mostrar_grafico_barras(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        self.driver.find_element(By.LINK_TEXT, "Ver").click()
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vo1.titulo).click()
        time.sleep(3)
        self.driver.find_element(By.ID, "enseñarBarra").click()
        time.sleep(3)
        self.assertEqual(self.driver.find_element(By.ID, "graficatarta").get_attribute("style"), "display: none;")


class TestGraficasVotacionPreferencia(StaticLiveServerTestCase):
    def setUp(self):
        q = Question(desc = "Aquí tiene su pregunta: ")
        q.save()

        self.vp1=VotacionPreferencia(id=1, titulo="Viva el Sevilla", fecha_inicio=datetime.datetime(2020, 7, 6), fecha_fin=datetime.datetime(2021, 7, 6))
        self.vp1.save()

        self.user = User(id = 1, username='Manuel', is_staff=True)
        self.user.set_password('contraseña')
        self.user.save()
        self.c = Census(id=1, voting_id=1, voter_id = 1)
        self.c.save()

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
  
    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        self.c=None
        self.user=None

        self.vp1=None

    def test_mostrar_grafico_sectores(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        self.driver.find_element_by_css_selector("tr:nth-child(2) .btn").click()
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vp1.titulo).click()
        time.sleep(3)
        self.driver.find_element(By.ID, "enseñarTarta").click()
        time.sleep(3)
        self.assertEqual(self.driver.find_element(By.ID, "graficabarras").get_attribute("style"), "display: none;")

    def test_mostrar_grafico_barras(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        self.driver.find_element_by_css_selector("tr:nth-child(2) .btn").click()
        time.sleep(3)
        self.driver.find_element_by_link_text(self.vp1.titulo).click()
        time.sleep(3)
        self.driver.find_element(By.ID, "enseñarBarra").click()
        time.sleep(3)
        self.assertEqual(self.driver.find_element(By.ID, "graficatarta").get_attribute("style"), "display: none;")