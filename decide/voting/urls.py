from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),

    path('votacionBinaria/<id>/', views.getVotacionBinariaById, name='Votacion Binaria'),
    path('votacionBinaria/all', views.getAllVotacionesBinarias, name='Votacion Binaria Todas'),

    path('downloadBinaria/<id>', views.downloadVotacionBinaria, name='Download Binaria'),
    path('downloadBinariaAll', views.downloadAllVotacionBinaria, name='Download Binaria All'),

    path('votacion/<id>/', views.getVotacionById, name='Votacion'),
    path('votacion/all', views.getAllVotaciones, name='Votacion Todas'),

    path('downloadNormal/<id>', views.downloadVotacionNomral, name='Download Normal'),
    path('downloadNormalAll', views.downloadAllVotacionNormal, name='Downlaod Normal All'),

    path('votacionMultiple/<id>/', views.getVotacionMultipleById, name='Votacion Multiple'),
    path('votacionMultiple/all', views.getAllVotacionesMultiples, name='Votacion Multiple Todas'),

    path('downloadMultiple/<id>', views.downloadVotacionMultiple, name='Download Multiple'),
    path('downloadMultipleAll', views.downloadAllVotacionMultiple, name='Download Multiple All'),

    path('votacionPreferencia/<id>/', views.getVotacionPreferenciaById, name='Votacion Preferencia'),
    path('votacionPreferencia/all', views.getAllVotacionesPreferencia, name='Votacion Preferencia'),

    path('downloadPreferencia/<id>', views.downloadVotacionPreferencia, name='Download Preferencia'),
    path('downloadPreferenciaAll', views.downloadAllVotacionPreferencia, name='Download Preferencia All')
]
