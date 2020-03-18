import logging
from django import forms
from athletics import models
from geography.models import Venue

logger = logging.getLogger(__name__)


class MeetForm(forms.ModelForm):

    class Meta:
        model = models.Meet

    def __init__(self, *args, **kwargs):
        super(MeetForm, self).__init__(*args, **kwargs)


class MeetInstanceForm(forms.ModelForm):

    class Meta:
        model = models.MeetInstance

    def __init__(self, *args, **kwargs):
        super(MeetInstanceForm, self).__init__(*args, **kwargs)
