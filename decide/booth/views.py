import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'index.html'

