"""URLproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from URLproject import views

handler404 = views.error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('all/', views.all, name='all'),
    path('mine/', views.mine, name='mine'),
    path('delete/<int:linkid>', views.delete, name='delete'),
    url(r'^(?P<linkhash>[a-z0-9]+)$', views.redir, name='redir'),
]
