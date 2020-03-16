import logging
from django import forms


logger = logging.getLogger(__name__)


class MeetForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    meet_type = forms.ModelChoiceField()
    environment = forms.ModelChoiceField()
    championship = forms.BooleanField(initial=False)


class MeetInstanceForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    venue = forms.ModelChoiceField()
    timing_system = forms.ModelChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    data_file = forms.FileField()
    url = forms.URLField(required=False)
