from django import template

register = template.Library()


@register.tag
def parse(parser, token):
    """
    Parses a value as a template and prints or saves to a variable

    Usage:
    {% parse <template_value> [as <variable>] %} %}

    Examples:
        {% parse object.description %}
        {% parse header as header %}
        {% parse "Hello, my name is {{ user.first_name }} {{ user.last_name }}" as greeting %}
    """
    bits = token.split_contents()
    tag_name = bits.pop(0)
    try:
        template_value = bits.pop(0)
        var_name = None
        if len(bits) >= 2:
            str_as, var_name = bits[:2]
    except (ValueError, IndexError):
        raise template.TemplateSyntaxError(f" { tag_name } tag requires the following syntax: " f"{{% { tag_name } <template_value> [as <variable>] %}}" )
    return ParseNode(template_value, var_name)


class ParseNode(template.Node):

    def __init__(self, template_value, var_name):
        self.template_value = template.Variable(template_value)
        self.var_name = var_name

    def render(self, context):
        try:
            template_value = self.template_value.resolve(context)
        except template.VariableDoesNotExist:
            template_value = self.template_value

        t = template.Template(template_value)
        context_variables = {}
        for d in list(context):
            for variable, value in d.items():
                context_variables[variable] = value

        request_context = template.RequestContext(context["request"], context_variables)
        result = t.render(request_context)
        if self.var_name:
            context[self.var_name] = result
            result = ""
        return result


@register.filter
def duration(value):
    """
    Arguments:
        value (int|float): Time in seconds

    Returns:
        str:  in the form of HH:MM:SS.MMMMM
    """
    raw_seconds = float(value)

    if not raw_seconds:
        return '00.00'

    milliseconds = int((value * 1000) % 1000)
    seconds = int(raw_seconds % 60)
    minutes = int((raw_seconds / 60) % 60)
    hours = int((raw_seconds / 3600) % 24)

    output = ''
    units = (hours, minutes, seconds)
    unit_lengths = (2, 2, 2)
    for unit, length in zip(units, unit_lengths):
        if output or unit:
            if output:
                output += ':'
            output += ('%d' % unit).zfill(length)

    output += '.'
    if milliseconds:
        output += ('%d' % milliseconds).strip('0')
    else:
        output += '00'
    return output


@register.filter
def distance(value):
    output = float(value)
    return '%sm' % value
