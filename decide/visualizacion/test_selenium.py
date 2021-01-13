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

from voting.models import *

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

    def test_visualizerIndexDefault(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_css_selector("tr:nth-child(5) .btn").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/default/".format(self.live_server_url))
        time.sleep(3)
        self.driver.find_element_by_link_text(self.v2.name).click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/{}/".format(self.live_server_url, self.v2.id))

class TestBinaryGraphs(StaticLiveServerTestCase):
    def setUp(self):
        #creamos la votacion        
        self.votacion = VotacionBinaria(titulo='titulo binario test',descripcion='desc binario test',fecha_inicio=datetime.datetime(2020, 7, 5), fecha_fin=datetime.datetime(2020, 7, 6))
        self.votacion.save()
        self.votacion2 = VotacionBinaria(titulo="titulo binario test 2", descripcion="desc binario test 2",fecha_inicio=datetime.datetime(2020, 7, 5), fecha_fin=datetime.datetime(2020, 7, 6))
        self.votacion2.save()
        #creamos la pregunta
        q = Question(desc = "Aquí tiene su pregunta: ")
        q.save()
        #creamos las respuestas
        r1  = RespuestaBinaria(respuesta = 1)
        r2  = RespuestaBinaria(respuesta = 0)
        r3 = RespuestaBinaria(respuesta = 1)

        self.votacion.addRespuestaBinaria(r1)
        self.votacion.addRespuestaBinaria(r2)
        self.votacion.addRespuestaBinaria(r3)


        #creamos el web driver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
        super().setUp()
  
    def tearDown(self):
        self.driver.quit()
        self.votacion2=None
        self.votacion=None
        super().tearDown()
        
    def test_bin(self):
        self.driver.get(f'{self.live_server_url}/visualizer/binaria')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@id=\'app-visualizer\']/div/table/tbody/tr/th/a").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "container")
        self.driver.find_element(By.ID, "container2")
        self.driver.find_element(By.ID, "container3")
        self.driver.find_element(By.ID, "container4")