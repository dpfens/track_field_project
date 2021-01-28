from django.views.generic.base import View, TemplateView
from django.http import JsonResponse


# Create your views here.
class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
