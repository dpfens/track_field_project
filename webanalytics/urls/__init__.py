from django.urls import path
from webanalytics import views
from webanalytics.views import api

app_name = 'webanalytics'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/page-view', api.PageView.as_view(), name='page_view'),
    path('api/event', api.EventView.as_view(), name='event')
]
