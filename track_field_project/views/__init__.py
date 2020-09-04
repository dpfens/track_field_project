import logging
import json

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language_from_request

from track_field_project import settings


logger = logging.getLogger(__name__)


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html', dict())


class AboutView(View):

    def get(self, request):
        return render(request, 'about.html', dict())


# Create your views here.
@cache_page(60 * 15)
def js_settings(request):
    JS_SETTINGS_TEMPLATE = """window.settings = JSON.parse('{{ json_data|safe }}');"""
    data = {
        "STATIC_URL": settings.STATIC_URL,
        "DEBUG": settings.DEBUG,
        "DEFAULT_LANGUAGE_CODE": settings.LANGUAGE_CODE,
        "CURRENT_LANGUAGE_CODE": get_language_from_request(request),
    }
    json_data = json.dumps(data)
    template = Template(JS_SETTINGS_TEMPLATE)
    context = Context({"json_data": json_data})
    response = HttpResponse(
        content=template.render(context),
        content_type="application/javascript; charset=UTF-8",
    )
    return response
