"""frontend URL Configuration

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
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView

# this triggers the registration of the apps
import frontend.map
import frontend.classify

app_name = "BDSE2"

urlpatterns = [
    url('^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url('^map', TemplateView.as_view(template_name='map.html'), name="map"),
    url('^classify', TemplateView.as_view(template_name='classify.html'), name="classify"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    url(r'^admin/', admin.site.urls)
]
