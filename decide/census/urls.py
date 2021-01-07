from django.urls import path, include
from . import views
from census.views import importCensusFromLdap

urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    #Url correspondiente al formulario de importación de LDAP
    path('addLDAPcensus', importCensusFromLdap, name='addLDAPcensus'),
    path('votings/<int:voter_id>/', views.ListVotingsByVoter.as_view(), name='census_votings'),
]

