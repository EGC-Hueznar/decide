from django.urls import path, re_path, include
from . import views
from .views import importar
from census.views import importCensusFromLdap


urlpatterns = [
    re_path('^(?P<type>VB|V|VP|VM|Vo)/$', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import', importar, name='import'),
    path('addLDAPcensus', importCensusFromLdap, name='addLDAPcensus'),
    path('votings/<int:voter_id>/', views.ListVotingsByVoter.as_view(), name='census_votings'),
    path('export/', views.fullExport, name='census_fullexport'),
    path('export/<int:voting_id>/', views.export, name='centus_export')
]

