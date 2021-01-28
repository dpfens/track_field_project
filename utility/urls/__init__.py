from django.urls import path
from utility import views


app_name = 'utility'
urlpatterns = [
    path('feedback/', views.FeedbackListView.as_view(), name='feedback'),
    path('feedback/int:id/', views.FeedbackDetail.as_view(), name='feedback_detail'),
    path('feedback/archive/', views.feedback_index_view, name='feedback_archive')
]
