from django import forms
import models


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = models.Feedback
        fields = ('content', 'feedback_type')
