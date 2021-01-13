from django.urls import path, include
from . import views
from .views import importar
from census.views import *


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import', importar, name='import'),
    #Url correspondiente al formulario de importación de LDAP
    path('addLDAPcensusBinaria', importCensusFromLdapBinaria, name='addLDAPcensus'),
    path('addLDAPcensusMultiple', importCensusFromLdapMultiple, name='addLDAPcensus'),
    path('addLDAPcensusPreferencia', importCensusFromLdapPreferencia, name='addLDAPcensus'),
    path('addLDAPcensusVotacion', importCensusFromLdapVotacion, name='addLDAPcensus'),
    path('votings/<int:voter_id>/', views.ListVotingsByVoter.as_view(), name='census_votings'),
    path('export/', views.fullExport, name='census_fullexport'),
    path('export/<int:voting_id>/', views.export, name='centus_export')
]

