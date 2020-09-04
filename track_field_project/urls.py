"""track_field_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from track_field_project.admin.site import advanced_admin
from track_field_project import views
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path(r'', views.IndexView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('account/', include('identity.urls')),
    path('js-settings.js', views.js_settings, name='js_settings'),
    path('admin/', admin.site.urls),
    path('advanced-admin/', advanced_admin.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
]
