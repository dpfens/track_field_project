import logging
from django import forms
from athletics import models
from identity.models import Identity


logger = logging.getLogger(__name__)


class PerformanceForm(forms.ModelForm):

    class Meta:
        model = models.Performance

    def __init__(self, *args, **kwargs):
        super(PerformanceForm, self).__init__(*args, **kwargs)
        identity = kwargs.pop('identity', dict())
        organization = kwargs.pop('organization', dict())
        super(PerformanceForm, self).__init__(*args, **kwargs)
        if identity:
            self.fields['identity'].queryset = Identity.objects.filter(**identity)
        if organization:
            self.fields['organization'].queryset = Identity.objects.filter(**organization)


class AttemptForm(forms.ModelForm):

    class Meta:
        model = models.Attempt

    def __init__(self, *args, **kwargs):
        super(AttemptForm, self).__init__(*args, **kwargs)


class SequentialAttemptForm(forms.ModelForm):

    class Meta:
        model = models.AttemptSequential

    def __init__(self, *args, **kwargs):
        super(SequentialAttemptForm, self).__init__(*args, **kwargs)


class ThresholdAttemptForm(forms.ModelForm):

    class Meta:
        model = models.AttemptThreshold

    def __init__(self, *args, **kwargs):
        super(ThresholdAttemptForm, self).__init__(*args, **kwargs)


class SplitForm(forms.ModelForm):

    class Meta:
        model = models.Split

    def __init__(self, *args, **kwargs):
        super(SplitForm, self).__init__(*args, **kwargs)
