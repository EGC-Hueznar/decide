from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostProcView.as_view(), name='postproc'),
    path('votacionBinaria/<id>',views.vistaBinaria),
    path('votacionBinaria/all/',views.vistaBinariaAll),
    path('votacion/<id>',views.vistaNormal),
    path('votacion/all/',views.vistaNormalAll),
    path('votacionMultiple/<id>',views.vistaMultiple),
    path('votacionMultiple/all/',views.vistaMultipleAll),
    path('votacionPreferencia/<id>',views.vistaPreferencia),
    path('votacionPreferencia/all/',views.vistaPreferenciaAll)
]
