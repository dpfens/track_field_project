from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
class DashboardView(TemplateView, PermissionRequiredMixin):
    permission_required = 'is_staff'

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
