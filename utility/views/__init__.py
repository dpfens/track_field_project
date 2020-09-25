import logging

from django.shortcuts import render
from django.views.decorators.cache import cache_page


logger = logging.getLogger(__name__)


def components_view(request):
    return render(request, 'components.html', dict())
