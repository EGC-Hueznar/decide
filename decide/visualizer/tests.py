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

    # Test de envío de reporte de una votación a Telegram
    def test_send_telegram_report(self):
        v = VotingTestCase.create_voting(self)
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

class VisualizerContextTestCase(BaseTestCase):

    def setUp(self):
        q = Question(desc="¿Que es el arte?")
        q.save()

        opt1 = QuestionOption(question=q, option="La expresión de los sentimientos de una persona en una composición artística")
        opt1.save()

        opt2 = QuestionOption(question=q, option="Morirte de frio")
        opt2.save()

        self.v = Voting(name="El arte", question=q)
        self.v.do_postproc()

        super().setUp()

    def tearDown(self):
        self.v=None

        super().tearDown()
  
    # Test método get_context_data de visualizer/views.py
    def test_context_data_API(self):

        self.login()
        data = {
            'name':'Example',
            'desc':'Descriçao',
            'question':'La caca',
            'question_opt':['se come', 'se bebe', 'se echa por el culo']
        }
    #Creación de la votación
        response = self.client.post('/voting/', data, format='json')
        self.assertEquals(response.status_code,201)

        v = Voting.objects.get(name="Example")
    #Comprobación que la página se crea
        response = self.client.get('/visualizer/{}/'.format(v.id))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed('visualizer/visualizer.html')


        # self.asser

