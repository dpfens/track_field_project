import logging
from django import forms
from athletics import models


logger = logging.getLogger(__name__)


class HeatForm(forms.ModelForm):

    class Meta:
        model = models.Heat

    def __init__(self, *args, **kwargs):
        super(HeatForm, self).__init__(*args, **kwargs)
