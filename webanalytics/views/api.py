from django.views.generic.base import View
from django.http import JsonResponse


# Create your views here.
class PageView(View):

    def get(self, request):
        error = False
        data = dict(error=error)
        return JsonResponse(data)

    def post(self, request):
        error = False
        data = dict(error=error)
        return JsonResponse(data)


class EventView(View):

    def get(self, request):
        error = False
        data = dict(error=error)
        return JsonResponse(data)

    def post(self, request):
        error = False
        data = dict(error=error)
        return JsonResponse(data)
