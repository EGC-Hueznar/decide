import telegram
from django.test import TestCase
from base.tests import BaseTestCase
from voting.tests import *
from visualizer.telegrambot import *

# Create your tests here.
class VisualizerTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # Método para crear el objeto bot
    def create_bot(self):    
        bot_token = '1415070510:AAE49OJPu4viYNo5Tfov4vzkoIyeNf_JBr4'
        bot = telegram.Bot(bot_token)
        return bot

    # Test de creación y obtención de los datos del bot de telegram
    def test_create_bot_telegram(self):
        bot = self.create_bot()
        id = "decidehueznarbot"
        self.assertEqual(bot.username,id)

    # Test de envío de mensaje de texto al grupo de Telegram
    def test_send_message_telegram(self):
        bot = self.create_bot()
        id = -1001318632551
        message = bot.send_message(id,"Test de envío de mensaje de texto")
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    # Test de envío de reporte de una votación tipo voting a Telegram
    def test_send_telegram_report(self):
        v = VotingTestCase.create_voting(self)
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    class GuardaVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb = VotacionBinaria(titulo="titulo 1",descripcion="Descripcion 1")
        vb.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb=None
    def testExist(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 1")
        self.assertEquals(vb.titulo,"titulo 1")
        self.assertEquals(vb.descripcion,"Descripcion 1")