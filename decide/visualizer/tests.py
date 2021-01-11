from django.contrib.auth.models import User
from django.test import TestCase
from base.tests import BaseTestCase
from voting.models import *
import datetime
from census.models import Census
import telegram
from voting.tests import *
from visualizer.telegrambot import *


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
        self.assertTemplateUsed('visualizer/index.html')
    def test_visualizer_default(self):
        self.login()
        response = self.client.get('/visualizer/default', follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/listdefault.html')
        response = self.client.get('/visualizer/{}'.format(self.v1.id), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/visualizer.html')
        v1 = Voting.objects.get(name = "¿Te gusta EGC?")
        self.assertEqual(v1.name, "¿Te gusta EGC?")
    def test_visualizer_normal(self):
        self.login()
        response = self.client.get('/visualizer/normal', follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/list.html')
        response = self.client.get('/visualizer/normal/{}'.format(self.vo1.id), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/resultnormal.html')
        vo1 = Votacion.objects.get(titulo = "¿Te gusta EGC?")
        self.assertEqual(vo1.titulo, "¿Te gusta EGC?")
    def test_visualizer_preferencia(self):
        self.login()
        response = self.client.get('/visualizer/preferencia', follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/list.html')
        response = self.client.get('/visualizer/preferencia/{}'.format(self.vp2.id), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/resultpref.html')
        vp2 = Votacion.objects.get(titulo = "¿Te gusta PGPI?")
        self.assertEqual(vp2.titulo, "¿Te gusta PGPI?")
    def test_visualizer_multiple(self):
        self.login()
        response = self.client.get('/visualizer/multiple', follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/list.html')
        response = self.client.get('/visualizer/multiple/{}'.format(self.vm3.id), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/resultmul.html')
        vm3 = Votacion.objects.get(titulo = "¿Te gusta AII?")
        self.assertEqual(vm3.titulo, "¿Te gusta AII?")
    def test_visualizer_binaria(self):
        self.login()
        response = self.client.get('/visualizer/binaria', follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/list.html')
        response = self.client.get('/visualizer/binaria/{}'.format(self.vb2.id), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('visualizer/resultbin.html')
        vb2 = VotacionBinaria.objects.get(titulo = "¿Te gusta PGPI?")
        self.assertEqual(vb2.titulo, "¿Te gusta PGPI?")

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
