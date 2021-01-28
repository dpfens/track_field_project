import logging
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from utility.models import Feedback
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView



logger = logging.getLogger(__name__)


feedback_index_view = ArchiveIndexView.as_view(model=Feedback, date_field="created_at")


class FeedbackListView(ListView):
    model = Feedback

    def head(self, *args, **kwargs):
        last_entry = self.get_queryset().latest('created_at')
        response = HttpResponse()
        # RFC 1123 date format
        response['Last-Modified'] = last_entry.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

    def get(self, request, **kwargs):
        pass


class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Feedback.objects.all()
    date_field = "created_at"
    allow_future = True


class FeedbackDetail(DetailView):
    model = Feedback

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['feedback_list'] = Feedback.objects.all()
        return context
