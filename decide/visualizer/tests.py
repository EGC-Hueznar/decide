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


# Tests envíos de reporte Votación Binaria
class SendTelegramVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        v = VotacionBinaria(titulo="Votación Binaria Test 1",descripcion="Descripcion 1")
        v.save()
        v2 = VotacionBinaria(titulo="Votación Binaria Test 2", descripcion="Descripcion 2")
        v2.save()
        r1  = RespuestaBinaria(respuesta = 1)
        r2 = RespuestaBinaria(respuesta = 1)
        r3 = RespuestaBinaria(respuesta = 0)
        v2.addRespuestaBinaria(r1)
        v2.addRespuestaBinaria(r2)
        v2.addRespuestaBinaria(r3)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None
        self.v2=None
        self.r1=None
        self.r2=None
        self.r3=None
    # Test Votación Binaria Simple
    def test_send_telegram_report_b(self):
        v = VotacionBinaria.objects.get(titulo="Votación Binaria Test 1")
        message = send_telegram_report_binary(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    # Test Votación Binaria con Respuestas
    def test_send_telegram_report_br(self):
        v = VotacionBinaria.objects.get(titulo="Votación Binaria Test 2")
        message = send_telegram_report_binary(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")