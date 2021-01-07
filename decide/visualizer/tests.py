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
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    # Test Votación Binaria con Respuestas
    def test_send_telegram_report_br(self):
        v = VotacionBinaria.objects.get(titulo="Votación Binaria Test 2")
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

# Tests envíos de reporte Votación Normal
class SendTelegramVotacionNormalTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="Votación Normal Test 1",descripcion="Descripcion 1")
        v.save()
        v2 = Votacion(titulo="Votación Normal Test 2", descripcion="Descripcion 2")
        v2.save()
        q1  = Pregunta(textoPregunta = "Pregunta Normal 1")
        q2  = Pregunta(textoPregunta = "Pregunta Normal 2")
        r1 = Respuesta(respuesta = 2)
        r2 = Respuesta(respuesta = 10)
        v.addPregunta(q1)
        v.addPregunta(q2)
        q2.addRespuesta(r1)
        q2.addRespuesta(r2)
        
        
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None
        self.v2=None
        self.q1=None
        self.q2=None
        self.r1=None
        self.r2=None

    # Test Votación Normal Simple
    def test_send_telegram_report_n(self):
        v = Votacion.objects.get(titulo="Votación Normal Test 1")
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    # Test Votación Normal con Respuestas
    def test_send_telegram_report_nr(self):
        v = Votacion.objects.get(titulo="Votación Normal Test 2")
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

# Tests envíos de reporte Votación Preferencia
class SendTelegramVotacionPreferenciaTest(BaseTestCase):
    def setUp(self):
        v = VotacionPreferencia(titulo="Votación Preferencia Test 1",descripcion="Descripcion 1")
        v.save()
        v2 = VotacionPreferencia(titulo="Votación Preferencia Test 2", descripcion="Descripcion 2")
        v2.save()
        q1  = PreguntaPreferencia(textoPregunta = "Pregunta Preferencia 1")
        q2  = PreguntaPreferencia(textoPregunta = "Pregunta Preferencia 2")
        o1 = OpcionRespuesta(nombre_opcion = "Opcion Preferencia 1")
        o2 = OpcionRespuesta(nombre_opcion = "Opcion Preferencia 2")
        o3 = OpcionRespuesta(nombre_opcion = "Opcion Preferencia 1")
        o4 = OpcionRespuesta(nombre_opcion = "Opcion Preferencia 2")
        r1 = RespuestaPreferencia(orden_preferencia = 2)
        r2 = RespuestaPreferencia(orden_preferencia = 10)
        r3 = RespuestaPreferencia(orden_preferencia = 4)
        r4 = RespuestaPreferencia(orden_preferencia = 9)
        v.addPreguntaPreferencia(q1)
        v2.addPreguntaPreferencia(q2)
        q1.addOpcionRespuesta(o1)
        q1.addOpcionRespuesta(o2)
        q2.addOpcionRespuesta(o3)
        q2.addOpcionRespuesta(o4)
        o3.addRespuetaPreferencia(r1)
        o3.addRespuetaPreferencia(r2)
        o4.addRespuetaPreferencia(r3)
        o4.addRespuetaPreferencia(r4)
        
        
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None
        self.v2=None
        self.q1=None
        self.q2=None
        self.o1=None
        self.o2=None
        self.o3=None
        self.o4=None
        self.r1=None
        self.r2=None
        self.r3=None
        self.r4=None

    # Test Votación Preferencia Simple
    def test_send_telegram_report_p(self):
        v = VotacionPreferencia.objects.get(titulo="Votación Preferencia Test 1")
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")

    # Test Votación Preferencia con Respuestas
    def test_send_telegram_report_pr(self):
        v = VotacionPreferencia.objects.get(titulo="Votación Preferencia Test 2")
        message = send_telegram_report(v)
        self.assertEqual(message.chat.title,"Actualizaciones Decide Huéznar")