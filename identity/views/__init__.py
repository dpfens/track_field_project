from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountView(TemplateView, LoginRequiredMixin):
    template_name = "account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PreferenceView(TemplateView, LoginRequiredMixin):
    template_name = "preference.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(TemplateView, LoginRequiredMixin):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PrivacyView(TemplateView, LoginRequiredMixin):
    template_name = "privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
