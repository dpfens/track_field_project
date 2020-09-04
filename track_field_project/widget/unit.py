from django import forms


class DurationWidget(forms.TextInput):
    classes = 'duration-input'

    class Media:
        js = ('widgets/duration.js', )

    def get_context(self, name, value, attrs):
        context = super(DurationWidget, self).get_context(name, value, attrs)
        context['widget']['attrs'].setdefault('class', '')
        new_classes = ' '.join([self.classes, context['widget']['attrs']['class']])
        context['widget']['attrs']['class'] = new_classes
        return context


class MultiDurationWidget(forms.MultiWidget):
    classes = 'duration-input'
    template_name = 'forms/widgets/duration.html'
    supported_units = ('years', 'days', 'minutes', 'seconds', 'milliseconds')
    unit_max_digits = {
        'milliseconds': 3,
        'seconds': 2,
        'minutes': 2,
        'hours': 2,
        'days': 3,
        'years': 4
    }
    unit_max_values = {
        'milliseconds': 999,
        'seconds': 59,
        'minutes': 59,
        'hours': 23,
        'days': 364,
        'years': 999999
    }
    unit_placeholders = {
        'milliseconds': 'mmm',
        'seconds': 'SS',
        'minutes': 'MM',
        'hours': 'HH',
        'days': 'DDD',
        'years': 'YYYY'
    }

    class Media:
        css = {
            'all': ('widgets/duration.css', )
        }
        js = ('widgets/duration.js', )

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', 'en')
        units = kwargs.pop('units', self.supported_units)
        exclude = kwargs.pop('exclude', [])
        max_values = kwargs.pop('max_values', self.unit_max_values)
        max_digits = kwargs.pop('max_digits', self.unit_max_digits)
        placeholders = kwargs.pop('placeholders', self.unit_placeholders)

        subwidgets = []
        units = [unit for unit in units if unit not in exclude]
        for unit in units:
            placeholder = placeholders[unit]
            max_value = max_values.get(unit, 99999)
            max_digit = max_digits.get(unit, 4)
            attrs = dict(min=0, max=max_value, limit=max_digit, placeholder=placeholder, lang=lang)
            attrs['class'] = unit
            widget = forms.TextInput(attrs=attrs)
            subwidgets.append(widget)
        self.units = units
        super(DurationWidget, self).__init__(subwidgets, *args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super(DurationWidget, self).get_context(name, value, attrs)
        context['widget']['attrs'].setdefault('class', '')
        new_classes = ' '.join([self.classes, context['widget']['attrs']['class']])
        context['widget']['attrs']['class'] = new_classes
        return context

    def decompress(self, value):
        if value:
            return [int(item) for item in value.split(' ')]
        return [0 for _ in self.widgets]
