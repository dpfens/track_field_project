import logging
from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)


class AutocompleteWidget(Widget):
    template_name = 'widgets/autocomplete.html'

    def get_context(self, name, value, attrs=dict()):
        return {'widget': {
            'name': name,
            'value': value,
            'attrs': attrs
        }}

    def render(self, name, value, attrs=dict()):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)
