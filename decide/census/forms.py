from django import forms
from voting.models import *
from census.models import Census
from django.forms import ModelMultipleChoiceField

#Formulario para introducir los datos necesarios para el metodo de LDAP
class CensusAddLdapFormVotacion(forms.Form):
    #Atributos
    voting = forms.ModelChoiceField(label='Votación a la que desea añadir censo', empty_label="-", queryset=Votacion.objects.all().filter(fecha_inicio__isnull=True, fecha_fin__isnull=True), required=True,)
    urlLdap = forms.CharField(label='Url del servidor LDAP', widget=forms.TextInput(attrs={'placeholder': 'ldap.ServerUrl:Port'}), required=True)
    treeSufix = forms.CharField(label='Rama del arbol del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=YourDomain,dc=com'}), required=True)
    branch = forms.CharField(label='Rama a buscar del LDAP', widget=forms.TextInput(attrs={'placeholder': 'dc=YourDomain,dc=com'}), required=True)
    pwd = forms.CharField(label='Contraseña del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'Password'}), required=True)


class CensusAddLdapFormVotacionBinaria(forms.Form):
    #Atributos
    voting = forms.ModelChoiceField(label='Votación a la que desea añadir censo', empty_label="-", queryset=VotacionBinaria.objects.all().filter(fecha_inicio__isnull=True, fecha_fin__isnull=True), required=True,)
    urlLdap = forms.CharField(label='Url del servidor LDAP', widget=forms.TextInput(attrs={'placeholder': 'ldap.ServerUrl:Port'}), required=True)
    treeSufix = forms.CharField(label='Rama del arbol del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=YourDomain,dc=com'}), required=True)
    branch = forms.CharField(label='Rama a buscar del LDAP', widget=forms.TextInput(attrs={'placeholder': 'dc=YourDomain,dc=com'}), required=True)
    pwd = forms.CharField(label='Contraseña del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'Password'}), required=True)

class CensusAddLdapFormVotacionMultiple(forms.Form):
    #Atributos
    voting = forms.ModelChoiceField(label='Votación a la que desea añadir censo', empty_label="-", queryset=VotacionMultiple.objects.all().filter(fecha_inicio__isnull=True, fecha_fin__isnull=True), required=True,)
    urlLdap = forms.CharField(label='Url del servidor LDAP', widget=forms.TextInput(attrs={'placeholder': 'ldap.ServerUrl:Port'}), required=True)
    treeSufix = forms.CharField(label='Rama del arbol del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=YourDomain,dc=com'}), required=True)
    branch = forms.CharField(label='Rama a buscar del LDAP', widget=forms.TextInput(attrs={'placeholder': 'dc=YourDomain,dc=com'}), required=True)
    pwd = forms.CharField(label='Contraseña del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'Password'}), required=True)

class CensusAddLdapFormVotacionPreferencia(forms.Form):
    #Atributos
    voting = forms.ModelChoiceField(label='Votación a la que desea añadir censo', empty_label="-", queryset=VotacionPreferencia.objects.all().filter(fecha_inicio__isnull=True, fecha_fin__isnull=True), required=True,)
    urlLdap = forms.CharField(label='Url del servidor LDAP', widget=forms.TextInput(attrs={'placeholder': 'ldap.ServerUrl:Port'}), required=True)
    treeSufix = forms.CharField(label='Rama del arbol del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=YourDomain,dc=com'}), required=True)
    branch = forms.CharField(label='Rama a buscar del LDAP', widget=forms.TextInput(attrs={'placeholder': 'dc=YourDomain,dc=com'}), required=True)
    pwd = forms.CharField(label='Contraseña del administrador LDAP', widget=forms.TextInput(attrs={'placeholder': 'Password'}), required=True)
