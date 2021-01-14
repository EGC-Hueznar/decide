from django.urls import path, re_path, include
from . import views
from .views import importar
from census.views import *


urlpatterns = [
    re_path('^(?P<type>VB|V|VP|VM|Vo)/$', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import', importar, name='import'),
    #Url correspondiente al formulario de importación de LDAP
    path('addLDAPcensusBinaria/', importCensusFromLdapBinaria, name='addLDAPcensusBinaria'),
    path('addLDAPcensusMultiple/', importCensusFromLdapMultiple, name='addLDAPcensusMultiple'),
    path('addLDAPcensusPreferencia/', importCensusFromLdapPreferencia, name='addLDAPcensusPreferencia'),
    path('addLDAPcensusVotacion/', importCensusFromLdapVotacion, name='addLDAPcensusVotacion'),
    path('votings/<int:voter_id>/', views.ListVotingsByVoter.as_view(), name='census_votings'),
    path('export/', views.fullExport, name='census_fullexport'),
    re_path('^export/(?P<type>VB|V|VP|VM|Vo)/(?P<voting_id>[0-9]{1,})/$', views.export, name='census_export')
]

