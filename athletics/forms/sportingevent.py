import logging
from django import forms
from athletics import models

logger = logging.getLogger(__name__)


class SportingEventForm(forms.ModelForm):

    class Meta:
        model = models.SportingEvent
        exclude = ('id', 'slug', 'participants', 'expected_competitiveness', 'actual_competitiveness', 'expected_eliteness', 'actual_eliteness', 'created_at', 'created_by', 'last_modified_at', 'last_modified_by')

    def clean(self):
        cleaned_data = super(SportingEventForm, self).clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        venue = cleaned_data['venue']
        name = cleaned_data['name']

        existing_event = models.SportingEvent.objects.filter(name=name, start_date=start_date, end_date=end_date, venue=venue).first()

        if existing_event:
            self.add_error(None, 'This sporting event already exists')

        return cleaned_data


class
