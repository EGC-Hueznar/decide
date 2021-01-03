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

from voting.models import Voting, Question

from census.models import Census


class TestVisualizerIndex(StaticLiveServerTestCase):
    def setUp(self):
        q = Question(desc = "Aquí tiene su pregunta: ")
        q.save()
        self.v1=Voting(id=1, name="¿Te gusta EGC?", start_date=datetime.datetime(2020, 7, 6), question = q)
        self.v2=Voting(id=2, name="¿Te gusta PGPI?", question = q)
        self.v3=Voting(id=3, name="¿Te gusta AII?", start_date=datetime.datetime(2020, 10, 6), end_date=datetime.datetime(2021, 7, 6), question = q)
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
        self.v1=None
        self.v2=None
        self.v3=None
    def test_visualizerIndexOK(self):
        self.driver.get(f'{self.live_server_url}/visualizer/')
        time.sleep(3)
        self.driver.find_element_by_link_text("¿Te gusta EGC?").click()
        time.sleep(3)
        self.assertEqual(self.driver.current_url, "{}/visualizer/{}/".format(self.live_server_url, self.v1.id))
