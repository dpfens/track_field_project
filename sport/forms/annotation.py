import logging
from django import forms
from sport import models

logger = logging.getLogger(__name__)


class AnnotationForm(forms.ModelForm):

    class Meta:
        model = models.Annotation

    def __init__(self, *args, **kwargs):
        super(AnnotationForm, self).__init__(*args, **kwargs)


class AnnotationAttemptSequentialForm(forms.ModelForm):

    class Meta:
        model = models.AnnotationAttemptSequential

    def __init__(self, *args, **kwargs):
        super(AnnotationAttemptSequentialForm, self).__init__(*args, **kwargs)


class AnnotationAttemptThresholdForm(forms.ModelForm):

    class Meta:
        model = models.AnnotationAttemptThreshold

    def __init__(self, *args, **kwargs):
        super(AnnotationAttemptThresholdForm, self).__init__(*args, **kwargs)


class AnnotationSplitForm(forms.ModelForm):

    class Meta:
        model = models.AnnotationSplit

    def __init__(self, *args, **kwargs):
        super(AnnotationSplitForm, self).__init__(*args, **kwargs)
