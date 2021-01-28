from django.views.generic.base import TemplateView


class AddressComponentView(TemplateView):

    template_name = "address_component.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LocationView(TemplateView):

    template_name = "location.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
