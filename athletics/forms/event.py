import logging
from django import forms
from athletics import models
from geography.models import Venue

logger = logging.getLogger(__name__)


class DisciplineForm(forms.ModelForm):

    class Meta:
        model = models.Discipline

    def __init__(self, *args, **kwargs):
        super(DisciplineForm, self).__init__(*args, **kwargs)


class EventForm(forms.ModelForm):

    class Meta:
        model = models.Event

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)


class EventDistance(forms.ModelForm):

    class Meta:
        model = models.Eventdistance

    def __init__(self, *args, **kwargs):
        super(EventDistanceForm, self).__init__(*args, **kwargs)


class EventWeightForm(forms.ModelForm):

    class Meta:
        model = models.EventWeight

    def __init__(self, *args, **kwargs):
        super(EventWeightForm, self).__init__(*args, **kwargs)


class EventHurdlesForm(forms.ModelForm):

    class Meta:
        model = models.EventHurdles

    def __init__(self, *args, **kwargs):
        super(EventHurdlesForm, self).__init__(*args, **kwargs)
