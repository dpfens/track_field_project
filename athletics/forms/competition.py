import logging
from django import forms
from athletics import models


logger = logging.getLogger(__name__)


class CompetitionForm(forms.ModelForm):

    class Meta:
        model = models.Competition

    def __init__(self, *args, **kwargs):
        super(CompetitionForm, self).__init__(*args, **kwargs)