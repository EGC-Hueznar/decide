import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import *


#TEST VOTACIONES BINARIAS

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


class ActualizaVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb = VotacionBinaria(titulo="titulo 1",descripcion="Descripcion 1")
        vb.save()
        vb.titulo = "titulo 2"
        vb.descripcion = "descripcion 2"
        vb.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb=None
    def testActualizado(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 2")
        self.assertEquals(vb.titulo,"titulo 2")
        self.assertEquals(vb.descripcion,"descripcion 2")


class BorraVotacionBinariaTest(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="titulo 1",descripcion="Descripcion 1")
        vb1.save()
        vb2 = VotacionBinaria(titulo="titulo 2",descripcion="Descripcion 2")
        vb2.save()
        vb2.delete()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.vb2=None
    def testBorrado(self):
        totalVotaciones = len(VotacionBinaria.objects.all())
        self.assertEquals(totalVotaciones,1)


class AddRespuestaBinaria(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="titulo 1",descripcion="Descripcion 1")
        vb1.save()
        rb1  = RespuestaBinaria(respuesta = 1)
        vb1.addRespuestaBinaria(rb1)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.rb1=None
    def testAdd(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 1")
        rb = RespuestaBinaria.objects.get(votacionBinaria_id=vb.id)
        self.assertEquals(rb.respuesta,1)
        self.assertEquals(rb.votacionBinaria_id,vb.id)

class CuentaTruesYFalsesTest(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="titulo 1",descripcion="Descripcion 1")
        vb1.save()
        
        rb1 = RespuestaBinaria(respuesta=1)
        rb2 = RespuestaBinaria(respuesta=1)
        rb3 = RespuestaBinaria(respuesta=1)
        rb4 = RespuestaBinaria(respuesta=0)

        vb1.addRespuestaBinaria(rb1)
        vb1.addRespuestaBinaria(rb2)
        vb1.addRespuestaBinaria(rb3)
        vb1.addRespuestaBinaria(rb4)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vb1=None
        self.rb1=None
        self.rb2=None
        self.rb3=None
        self.rb4=None
    def testContador(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 1")
        self.assertEquals(vb.Numero_De_Trues(),3)
        self.assertEquals(vb.Numero_De_Falses(),1)

class testPostProcBinarias(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="titulo 1", descripcion="Descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        vb1.save()

        rb1 = RespuestaBinaria(respuesta=1)
        rb2 = RespuestaBinaria(respuesta=1)
        rb3 = RespuestaBinaria(respuesta=1)
        rb4 = RespuestaBinaria(respuesta=0)

        vb1.addRespuestaBinaria(rb1)
        vb1.addRespuestaBinaria(rb2)
        vb1.addRespuestaBinaria(rb3)
        vb1.addRespuestaBinaria(rb4)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.vb1 = None
        self.rb1 = None
        self.rb2 = None
        self.rb3 = None
        self.rb4 = None

    def testPostProc(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 1")
        vbJson = vb.doPostProc()
        self.assertEquals(vbJson["titulo"], vb.titulo)
        self.assertEquals(vbJson["descripcion"],vb.descripcion)
        self.assertEquals(vbJson["Inicio de la votacion"], str(vb.fecha_inicio))
        self.assertEquals(vbJson["Cierre de la votacion"], str(vb.fecha_fin))
        self.assertEquals(vbJson["Numero de respuetas a Sí"], vb.Numero_De_Trues())
        self.assertEquals(vbJson["Numero de respuetas a No"], vb.Numero_De_Falses())

class testToJsonbinarias(BaseTestCase):
    def setUp(self):
        vb1 = VotacionBinaria(titulo="titulo 1", descripcion="Descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        vb1.save()

        rb1 = RespuestaBinaria(respuesta=1)
        rb2 = RespuestaBinaria(respuesta=1)
        rb3 = RespuestaBinaria(respuesta=1)
        rb4 = RespuestaBinaria(respuesta=0)

        vb1.addRespuestaBinaria(rb1)
        vb1.addRespuestaBinaria(rb2)
        vb1.addRespuestaBinaria(rb3)
        vb1.addRespuestaBinaria(rb4)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.vb1 = None
        self.rb1 = None
        self.rb2 = None
        self.rb3 = None
        self.rb4 = None

    def testToJson(self):
        vb = VotacionBinaria.objects.get(titulo="titulo 1")
        vbJson = vb.toJson()
        self.assertEquals(vbJson["titulo"], vb.titulo)
        self.assertEquals(vbJson["descripcion"],vb.descripcion)
        self.assertEquals(vbJson["fecha_inicio"], str(vb.fecha_inicio))
        self.assertEquals(vbJson["fecha_fin"], str(vb.fecha_fin))
        respuestas = vb.respuestasBinarias.all()
        respuestasJson = vbJson['respuestas']
        for r,rj in zip(respuestas,respuestasJson):
            self.assertEquals(r.id,rj['id'])
            self.assertEquals(r.respuesta, rj['respuesta'])
#TEST VOTACIONES PREFERENCIAS
class GuardaVotacionPreferenciaTest(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
    def testExist(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        self.assertEquals(vp.titulo,"preferencia 1")
        self.assertEquals(vp.descripcion,"descripcion 1")


class ActualizaVotacionPreferenciaTest(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        vp.titulo = "preferencia 2"
        vp.descripcion = "descripcion 2"
        vp.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
    def testActualizado(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 2")
        self.assertEquals(vp.titulo,"preferencia 2")
        self.assertEquals(vp.descripcion,"descripcion 2")

class BorraVotacionPreferenciaTest(BaseTestCase):
    def setUp(self):
        vp1 = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp1.save()
        vp2 = VotacionPreferencia(titulo="preferencia 2",descripcion="descripcion 2")
        vp2.save()
        vp2.delete()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp1=None
        self.vp2=None
    def testBorrado(self):
        totalVotaciones = len(VotacionPreferencia.objects.all())
        self.assertEquals(totalVotaciones,1)

class AddPreguntaPreferenciaTest(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        pp = PreguntaPreferencia.objects.get(votacionPreferencia_id=vp.id)
        self.assertEquals(pp.textoPregunta,"Texto 1")
        self.assertEquals(pp.votacionPreferencia_id,vp.id)

class CuentaPreguntaPreferencia(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp1 = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp1)
        pp2 = PreguntaPreferencia(textoPregunta ="Texto 2")
        vp.addPreguntaPreferencia(pp2)
        pp3 = PreguntaPreferencia(textoPregunta ="Texto 3")
        vp.addPreguntaPreferencia(pp3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp1=None
        self.pp2=None
        self.pp3=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        self.assertEquals(vp.Numero_De_Preguntas_Preferencia(),3)

class AddOpcionRespuestaTest(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        pp = PreguntaPreferencia.objects.get(votacionPreferencia_id=vp.id)
        opr = OpcionRespuesta.objects.get(preguntaPreferencia_id=pp.id)
        self.assertEquals(opr.nombre_opcion,"Opcion 1")
        self.assertEquals(opr.preguntaPreferencia_id,pp.id)

class CuentaOpcionesDePregunta(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr1 = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr1)
        opr2 = OpcionRespuesta(nombre_opcion = "Opcion 2")
        pp.addOpcionRespuesta(opr2)
        opr3 = OpcionRespuesta(nombre_opcion = "Opcion 3")
        pp.addOpcionRespuesta(opr3)
        opr4 = OpcionRespuesta(nombre_opcion = "Opcion 4")
        pp.addOpcionRespuesta(opr4)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr1=None
        self.opr2=None
        self.opr3=None
        self.opr4=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        pp = PreguntaPreferencia.objects.get(votacionPreferencia_id=vp.id)
        self.assertEquals(pp.Numero_De_Opciones(),4)

class AddRespuestaAOpcion(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr)
        rp = RespuestaPreferencia(orden_preferencia=1)
        opr.addRespuetaPreferencia(rp)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr=None
        self.rp=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        pp = PreguntaPreferencia.objects.get(votacionPreferencia_id=vp.id)
        opr = OpcionRespuesta.objects.get(preguntaPreferencia_id=pp.id)
        rp = RespuestaPreferencia.objects.get(opcionRespuesta_id=opr.id)
        self.assertEquals(rp.orden_preferencia,1)
        self.assertEquals(rp.opcionRespuesta_id,opr.id)


class EstadisticaOpcionPreferencia(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr)
        rp1 = RespuestaPreferencia(orden_preferencia=1)
        opr.addRespuetaPreferencia(rp1)
        rp2 = RespuestaPreferencia(orden_preferencia=2)
        opr.addRespuetaPreferencia(rp2)
        rp3 = RespuestaPreferencia(orden_preferencia=3)
        opr.addRespuetaPreferencia(rp3)
        rp4 = RespuestaPreferencia(orden_preferencia=2)
        opr.addRespuetaPreferencia(rp4)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr=None
        self.rp1=None
        self.rp2=None
        self.rp3=None
        self.rp4=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        pp = PreguntaPreferencia.objects.get(votacionPreferencia_id=vp.id)
        opr = OpcionRespuesta.objects.get(preguntaPreferencia_id=pp.id)

        respuesta = opr.Respuestas_Opcion()
        self.assertEquals(opr.Media_Preferencia(),2)
        self.assertEquals(respuesta[0][1],'1 veces')
        self.assertEquals(respuesta[1][1],'2 veces')
        self.assertEquals(respuesta[2][1],'1 veces')

class testPostProcPreferencia(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr)
        opr2 = OpcionRespuesta(nombre_opcion="Opcion 2")
        pp.addOpcionRespuesta(opr2)
        rp = RespuestaPreferencia(orden_preferencia=1)
        opr.addRespuetaPreferencia(rp)
        rp2 = RespuestaPreferencia(orden_preferencia=2)
        opr.addRespuetaPreferencia(rp2)
        rp3 = RespuestaPreferencia(orden_preferencia=1)
        opr2.addRespuetaPreferencia(rp3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr=None
        self.rp=None
    def testAdd(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        vpJson = vp.doPostProc()
        self.assertEquals(vpJson["titulo"], vp.titulo)
        self.assertEquals(vpJson["descripcion"], vp.descripcion)
        self.assertEquals(vpJson["Inicio de la votacion"], str(vp.fecha_inicio))
        self.assertEquals(vpJson["Cierre de la votacion"], str(vp.fecha_fin))

        preguntas = vp.preguntasPreferencia.all()
        preguntasJson = vpJson["preguntas"]

        for p,pj in zip(preguntas,preguntasJson):
            self.assertEquals(p.textoPregunta,pj['Pregunta'])
            opciones = p.opcionesRespuesta.all()
            opcionesJson = pj["Resultados de las opciones"]
            for o,oj in zip(opciones,opcionesJson):
                self.assertEquals(o.Media_Preferencia(), oj['Media de Preferencia de la opcion: '])
                self.assertEquals(str(o.Respuestas_Opcion()), oj['Votos dados a la opcion: '])

class testToJsonPreferencia(BaseTestCase):
    def setUp(self):
        vp = VotacionPreferencia(titulo="preferencia 1",descripcion="descripcion 1")
        vp.save()
        pp = PreguntaPreferencia(textoPregunta ="Texto 1")
        vp.addPreguntaPreferencia(pp)
        opr = OpcionRespuesta(nombre_opcion = "Opcion 1")
        pp.addOpcionRespuesta(opr)
        opr2 = OpcionRespuesta(nombre_opcion="Opcion 2")
        pp.addOpcionRespuesta(opr2)
        rp = RespuestaPreferencia(orden_preferencia=1)
        opr.addRespuetaPreferencia(rp)
        rp2 = RespuestaPreferencia(orden_preferencia=2)
        opr.addRespuetaPreferencia(rp2)
        rp3 = RespuestaPreferencia(orden_preferencia=1)
        opr2.addRespuetaPreferencia(rp3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vp=None
        self.pp=None
        self.opr=None
        self.rp=None
    def testJson(self):
        vp = VotacionPreferencia.objects.get(titulo="preferencia 1")
        vpJson = vp.toJson()
        self.assertEquals(vpJson["titulo"], vp.titulo)
        self.assertEquals(vpJson["descripcion"], vp.descripcion)
        self.assertEquals(vpJson["fecha_inicio"], str(vp.fecha_inicio))
        self.assertEquals(vpJson["fecha_fin"], str(vp.fecha_fin))

        preguntas = vp.preguntasPreferencia.all()
        preguntasJson = vpJson["preguntas"]

        for p,pj in zip(preguntas,preguntasJson):
            self.assertEquals(p.id, pj['id'])
            self.assertEquals(p.textoPregunta, pj['pregunta'])
            opciones = p.opcionesRespuesta.all()
            opcionesJson = pj["opciones"]
            for o,oj in zip(opciones,opcionesJson):
                self.assertEquals(o.id,oj["id"])
                self.assertEquals(o.nombre_opcion, oj["nombre_opcion"])
                respuestas = o.respuestasPreferencia.all()
                respuestasJson = oj["respuestas"]
                for r,rj in zip(respuestas,respuestasJson):
                    self.assertEquals(r.id, rj["id"])
                    self.assertEquals(r.orden_preferencia, rj["orden_preferencia"])

#TEST VOTACIONES NORMALES

class GuardaVotacionTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
    def testExist(self):
        v = Votacion.objects.get(titulo="votacion 1")
        self.assertEquals(v.titulo,"votacion 1")
        self.assertEquals(v.descripcion,"descripcion 1")


class ActualizaVotacionTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        v.titulo = "votacion 2"
        v.descripcion = "descripcion 2"
        v.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
    def testActualizado(self):
        v = Votacion.objects.get(titulo="votacion 2")
        self.assertEquals(v.titulo,"votacion 2")
        self.assertEquals(v.descripcion,"descripcion 2")

class BorraVotacionTest(BaseTestCase):
    def setUp(self):
        v1 = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v1.save()
        v2 = Votacion(titulo="votacion 2",descripcion="descripcion 2")
        v2.save()
        v2.delete()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v1=None
        self.v2=None
    def testBorrado(self):
        totalVotaciones = len(Votacion.objects.all())
        self.assertEquals(totalVotaciones,1)

class AddPreguntaTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        p = Pregunta(textoPregunta ="Texto 1")
        v.addPregunta(p)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p=None
    def testAdd(self):
        v = Votacion.objects.get(titulo="votacion 1")
        p = Pregunta.objects.get(votacion_id=v.id)
        self.assertEquals(p.textoPregunta,"Texto 1")
        self.assertEquals(p.votacion_id,v.id)

class CuentaPreguntas(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        p1 = Pregunta(textoPregunta ="Texto 1")
        p2 = Pregunta(textoPregunta ="Texto 2")
        p3 = Pregunta(textoPregunta ="Texto 3")
        v.addPregunta(p1)
        v.addPregunta(p2)
        v.addPregunta(p3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p1=None
        self.p2=None
        self.p3=None
    def testContador(self):
        v = Votacion.objects.get(titulo="votacion 1")
        self.assertEquals(v.Numero_De_Preguntas(),3)
        
class AddRespuestaTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        p = Pregunta(textoPregunta ="Texto 1")
        v.addPregunta(p)
        r1 = Respuesta(respuesta = 7)
        p.addRespuesta(r1)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p=None
        self.r1=None
    def testAdd(self):
        v = Votacion.objects.get(titulo="votacion 1")
        p = Pregunta.objects.get(votacion_id=v.id)
        r = Respuesta.objects.get(pregunta_id=p.id)
        self.assertEquals(r.respuesta,7)
        self.assertEquals(r.pregunta_id,p.id)

class EstadisticasRespuestasTest(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1")
        v.save()
        p = Pregunta(textoPregunta ="Texto 1")
        v.addPregunta(p)
        r1 = Respuesta(respuesta = 7)
        p.addRespuesta(r1)
        r2 = Respuesta(respuesta = 5)
        p.addRespuesta(r2)
        r3 = Respuesta(respuesta = 1)
        p.addRespuesta(r3)
        r4 = Respuesta(respuesta = 3)
        p.addRespuesta(r4)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p=None
        self.r1=None
        self.r2=None
        self.r3=None
        self.r4=None
    def testAdd(self):
        v = Votacion.objects.get(titulo="votacion 1")
        p = Pregunta.objects.get(votacion_id=v.id)
        self.assertEquals(p.Numero_De_Respuestas(),4)
        self.assertEquals(p.Media_De_Las_Respuestas(),4)
        self.assertEquals(p.Respuesta_Maxima(),"7")
        self.assertEquals(p.Respuesta_Minima(),"1")

class testPostProcNormales(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        v.save()
        p = Pregunta(textoPregunta ="Texto 1")
        v.addPregunta(p)
        r1 = Respuesta(respuesta = 7)
        p.addRespuesta(r1)
        r2 = Respuesta(respuesta=5)
        p.addRespuesta(r2)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p=None
        self.r1=None
        self.r2=None
    def testPostProc(self):
        v = Votacion.objects.get(titulo="votacion 1")
        vJson = v.doPostProc()
        self.assertEquals(vJson["titulo"], v.titulo)
        self.assertEquals(vJson["descripcion"], v.descripcion)
        self.assertEquals(vJson["Inicio de la votacion"], str(v.fecha_inicio))
        self.assertEquals(vJson["Cierre de la votacion"], str(v.fecha_fin))

        preguntasJson = vJson["preguntas"]
        preguntas = v.preguntas.all()

        for p,pj in zip(preguntas,preguntasJson):
            self.assertEquals(p.textoPregunta,pj['Pregunta'])
            self.assertEquals(p.Media_De_Las_Respuestas(), pj['Respuesta Media'])
            self.assertEquals(p.Respuesta_Maxima(), pj['Respuesta Maxima'])
            self.assertEquals(p.Respuesta_Minima(), pj['Respuesta Minima'])

class testJsonNormales(BaseTestCase):
    def setUp(self):
        v = Votacion(titulo="votacion 1",descripcion="descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        v.save()
        p = Pregunta(textoPregunta ="Texto 1")
        v.addPregunta(p)
        r1 = Respuesta(respuesta = 7)
        p.addRespuesta(r1)
        r2 = Respuesta(respuesta=5)
        p.addRespuesta(r2)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.v=None
        self.p=None
        self.r1=None
        self.r2=None
    def testJson(self):
        v = Votacion.objects.get(titulo="votacion 1")
        vJson = v.toJson()
        self.assertEquals(vJson["titulo"], v.titulo)
        self.assertEquals(vJson["descripcion"], v.descripcion)
        self.assertEquals(vJson["fecha_inicio"], str(v.fecha_inicio))
        self.assertEquals(vJson["fecha_fin"], str(v.fecha_fin))

        preguntasJson = vJson["preguntas"]
        preguntas = v.preguntas.all()

        for p,pj in zip(preguntas,preguntasJson):
           self.assertEquals(p.id,pj['id'])
           self.assertEquals(p.textoPregunta, pj['pregunta'])
           respuestas = p.respuestas.all()
           respuestasJson = pj["respuestas"]
           for r,rj in zip(respuestas,respuestasJson):
               self.assertEquals(r.id, rj['id'])
               self.assertEquals(r.respuesta, rj['respuesta'])

#TEST VOTACIONES MULTIPLES
class GuardaVotacionMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="titulo 1",descripcion="Descripcion 1")
        vm.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
    def testExist(self):
        vm = VotacionMultiple.objects.get(titulo="titulo 1")
        self.assertEquals(vm.titulo,"titulo 1")
        self.assertEquals(vm.descripcion,"Descripcion 1")


class ActualizaVotacionMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="titulo 1",descripcion="Descripcion 1")
        vm.save()
        vm.titulo = "titulo 2"
        vm.descripcion = "descripcion 2"
        vm.save()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
    def testActualizado(self):
        vm = VotacionMultiple.objects.get(titulo="titulo 2")
        self.assertEquals(vm.titulo,"titulo 2")
        self.assertEquals(vm.descripcion,"descripcion 2")


class BorraVotacionMultipleTest(BaseTestCase):
    def setUp(self):
        vm1 = VotacionMultiple(titulo="titulo 1",descripcion="Descripcion 1")
        vm1.save()
        vm2 = VotacionMultiple(titulo="titulo 2",descripcion="Descripcion 2")
        vm2.save()
        vm2.delete()
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm1=None
        self.vm2=None
    def testBorrado(self):
        totalVotacionesMultiples = len(VotacionMultiple.objects.all())
        self.assertEquals(totalVotacionesMultiples,1)

class AddPreguntaMultiple(BaseTestCase):
    def setUp(self):
        vm1 = VotacionMultiple(titulo="titulo 1",descripcion="Descripcion 1")
        vm1.save()
        pm1  = PreguntaMultiple(textoPregunta="pregunta 1")
        vm1.addPreguntaMultiple(pm1)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm1=None
        self.pm1 =None
    def testAdd(self):
        vm = VotacionMultiple.objects.get(titulo="titulo 1")
        pm = PreguntaMultiple.objects.get(votacionMultiple_id=vm.id)
        self.assertEquals(pm.textoPregunta,"pregunta 1")
        self.assertEquals(pm.votacionMultiple_id,vm.id)

class CuentaPreguntasMultiples(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1",descripcion="descripcion 1")
        vm.save()
        pm1 = PreguntaMultiple(textoPregunta ="Texto 1")
        pm2 = PreguntaMultiple(textoPregunta ="Texto 2")
        pm3 = PreguntaMultiple(textoPregunta ="Texto 3")
        vm.addPreguntaMultiple(pm1)
        vm.addPreguntaMultiple(pm2)
        vm.addPreguntaMultiple(pm3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
        self.pm1=None
        self.pm2=None
        self.pm3=None
    def testContador(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        self.assertEquals(vm.Numero_De_Preguntas_Multiple(),3)

class AddOpcionMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1",descripcion="descripcion 1")
        vm.save()
        pm = PreguntaMultiple(textoPregunta ="Texto 1")
        vm.addPreguntaMultiple(pm)
        om1 = OpcionMultiple(nombre_opcion = "Opcion 1",n_votado=0)
        pm.addOpcionMultiple(om1)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
        self.pm=None
        self.om1=None
    def testAdd(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        pm = PreguntaMultiple.objects.get(votacionMultiple_id=vm.id)
        om = OpcionMultiple.objects.get(preguntaMultiple_id=pm.id)
        self.assertEquals(om.nombre_opcion,"Opcion 1")
        self.assertEquals(om.preguntaMultiple_id,pm.id)
        self.assertEquals(om.n_votado,0)


class numeroOpcionesPreguntaMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1", descripcion="descripcion 1")
        vm.save()
        pm = PreguntaMultiple(textoPregunta="Texto 1")
        vm.addPreguntaMultiple(pm)
        om1 = OpcionMultiple(nombre_opcion="Opcion 1", n_votado=0)
        pm.addOpcionMultiple(om1)
        om2 = OpcionMultiple(nombre_opcion="Opcion 2", n_votado=1)
        pm.addOpcionMultiple(om2)
        om3 = OpcionMultiple(nombre_opcion="Opcion 3", n_votado=10)
        pm.addOpcionMultiple(om3)
        om4 = OpcionMultiple(nombre_opcion="Opcion 4", n_votado=20)
        pm.addOpcionMultiple(om4)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.vm = None
        self.pm = None
        self.om1 = None
        self.om2 = None
        self.om3 = None
        self.om4 = None

    def testAdd(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        pm = PreguntaMultiple.objects.get(votacionMultiple_id=vm.id)
        self.assertEquals(pm.Numero_De_Opciones(), 4)


class presentaOpcionesPreguntaMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1", descripcion="descripcion 1")
        vm.save()
        pm = PreguntaMultiple(textoPregunta="Texto 1")
        vm.addPreguntaMultiple(pm)
        om1 = OpcionMultiple(nombre_opcion="Opcion 1", n_votado=0)
        pm.addOpcionMultiple(om1)
        om2 = OpcionMultiple(nombre_opcion="Opcion 2", n_votado=1)
        pm.addOpcionMultiple(om2)
        om3 = OpcionMultiple(nombre_opcion="Opcion 3", n_votado=10)
        pm.addOpcionMultiple(om3)
        om4 = OpcionMultiple(nombre_opcion="Opcion 4", n_votado=20)
        pm.addOpcionMultiple(om4)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.vm = None
        self.pm = None
        self.om1 = None
        self.om2 = None
        self.om3 = None
        self.om4 = None

    def testAdd(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        pm = PreguntaMultiple.objects.get(votacionMultiple_id=vm.id)
        presentacionOpciones = pm.cuentaOpcionesMultiple()
        self.assertEquals(presentacionOpciones['Opcion 1'], 0)
        self.assertEquals(presentacionOpciones['Opcion 2'], 1)
        self.assertEquals(presentacionOpciones['Opcion 3'], 10)
        self.assertEquals(presentacionOpciones['Opcion 4'], 20)


class votaVariasOpcionesPreguntaMultipleTest(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1", descripcion="descripcion 1")
        vm.save()
        pm = PreguntaMultiple(textoPregunta="Texto 1")
        vm.addPreguntaMultiple(pm)
        om1 = OpcionMultiple(nombre_opcion="Opcion 1", n_votado=0)
        om2 = OpcionMultiple(nombre_opcion="Opcion 2", n_votado=1)
        om3 = OpcionMultiple(nombre_opcion="Opcion 3", n_votado=10)
        om4 = OpcionMultiple(nombre_opcion="Opcion 4", n_votado=20)
        listaOpciones = [om1, om2, om3, om4]
        pm.votaOpcioneMultiples(listaOpciones)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.vm = None
        self.pm = None
        self.om1 = None
        self.om2 = None
        self.om3 = None
        self.om4 = None

    def testAdd(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        pm = PreguntaMultiple.objects.get(votacionMultiple_id=vm.id)
        presentacionOpciones = pm.cuentaOpcionesMultiple()
        self.assertEquals(pm.Numero_De_Opciones(), 4)
        self.assertEquals(presentacionOpciones['Opcion 1'], 1)
        self.assertEquals(presentacionOpciones['Opcion 2'], 2)
        self.assertEquals(presentacionOpciones['Opcion 3'], 11)
        self.assertEquals(presentacionOpciones['Opcion 4'], 21)

class testPostProcMultiple(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1",descripcion="descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        vm.save()
        pm = PreguntaMultiple(textoPregunta ="Texto 1")
        vm.addPreguntaMultiple(pm)
        pm2 = PreguntaMultiple(textoPregunta="Texto 2")
        vm.addPreguntaMultiple(pm2)
        om1 = OpcionMultiple(nombre_opcion = "Opcion 1",n_votado=0)
        pm.addOpcionMultiple(om1)
        om2 = OpcionMultiple(nombre_opcion="Opcion 2", n_votado=3)
        pm.addOpcionMultiple(om2)
        om3 = OpcionMultiple(nombre_opcion="Opcion3", n_votado=7)
        pm2.addOpcionMultiple(om3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
        self.pm=None
        self.om1=None
    def testPostProc(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        vmJson = vm.doPostProc()
        self.assertEquals(vmJson["titulo"], vm.titulo)
        self.assertEquals(vmJson["descripcion"], vm.descripcion)
        self.assertEquals(vmJson["Inicio de la votacion"], str(vm.fecha_inicio))
        self.assertEquals(vmJson["Cierre de la votacion"], str(vm.fecha_fin))

        preguntas = vm.preguntasMultiples.all()
        preguntasJson = vmJson["preguntas"]

        for p,pj in zip(preguntas,preguntasJson):
            self.assertEquals(p.textoPregunta,pj['Pregunta'])
            opciones = p.opcionesMultiples.all()
            opcionesJson = pj['Resultados de las opciones']
            for o,oj in zip(opciones,opcionesJson):
                self.assertEquals(o.n_votado, oj['Numero de veces que se ha votado '+o.nombre_opcion])

class testJsonMultiple(BaseTestCase):
    def setUp(self):
        vm = VotacionMultiple(titulo="votacion 1",descripcion="descripcion 1",fecha_inicio=timezone.now(),fecha_fin=timezone.now())
        vm.save()
        pm = PreguntaMultiple(textoPregunta ="Texto 1")
        vm.addPreguntaMultiple(pm)
        pm2 = PreguntaMultiple(textoPregunta="Texto 2")
        vm.addPreguntaMultiple(pm2)
        om1 = OpcionMultiple(nombre_opcion = "Opcion 1",n_votado=0)
        pm.addOpcionMultiple(om1)
        om2 = OpcionMultiple(nombre_opcion="Opcion 2", n_votado=3)
        pm.addOpcionMultiple(om2)
        om3 = OpcionMultiple(nombre_opcion="Opcion3", n_votado=7)
        pm2.addOpcionMultiple(om3)
        super().setUp()
    def tearDown(self):
        super().tearDown()
        self.vm=None
        self.pm=None
        self.om1=None
    def testPostProc(self):
        vm = VotacionMultiple.objects.get(titulo="votacion 1")
        vmJson = vm.toJson()
        self.assertEquals(vmJson["titulo"], vm.titulo)
        self.assertEquals(vmJson["descripcion"], vm.descripcion)
        self.assertEquals(vmJson["fecha_inicio"], str(vm.fecha_inicio))
        self.assertEquals(vmJson["fecha_fin"], str(vm.fecha_fin))

        preguntas = vm.preguntasMultiples.all()
        preguntasJson = vmJson["preguntas"]

        for p,pj in zip(preguntas,preguntasJson):
            self.assertEquals(p.id, pj['id'])
            self.assertEquals(p.textoPregunta,pj['pregunta'])
            opciones = p.opcionesMultiples.all()
            opcionesJson = pj['opciones']
            for o,oj in zip(opciones,opcionesJson):
                self.assertEquals(o.id, oj['id'])
                self.assertEquals(o.nombre_opcion, oj['opcion'])
                self.assertEquals(o.n_votado, oj['n_votado'])

class VotingModelTC(BaseTestCase):
    def setUp(self):
        q=Question(desc="Descripcion")
        q.save()

        opt1= QuestionOption(question=q, option="option1")
        opt1.save()

        opt2= QuestionOption(question=q, option="option2")
        opt2.save()

        self.v=Voting(name="Votacion",question=q)
        self.v.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.v=None

    def testExist(self):
        v = Voting.objects.get(name="Votacion")
        self.assertEquals(v.question.options.all()[0].option,"option1")

    def testCreateVotingAPI(self):
        self.login()
        data = {
            'name':'Example',
            'desc':'Descripcion',
            'question':'I wanna',
            'question_opt':['car','house','party']
        }

        response = self.client.post('/voting/',data,format='json')
        self.assertEqual(response.status_code,201)

        v = Voting.objects.get(name="Example")
        self.assertEqual(v.desc,'Descripcion')

class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_Voting_toString(self):
        v = self.create_voting()
        self.assertEquals(str(v),"test voting")
        self.assertEquals(str(v.question),"test question")
        self.assertEquals(str(v.question.options.all()[0]),"option 1 (2)")

    
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')