from django.urls import path
from utility import views

urlpatterns = [
    path('', views.components_view, name='index'),
    path('components', views.components_view, name='components'),
]
