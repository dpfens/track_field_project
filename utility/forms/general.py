from django import forms
import models


class GenericFeedbackForm(forms.Form):
    feedback_type = models.ModelChoiceField(queryset=models.FeedbackType.objects.all())
    content = models.TextField()


class AnonymousFeedbackForm(GenericFeedbackForm):
    email_address = forms.CharField(max_length=100)
