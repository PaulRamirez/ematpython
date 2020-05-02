"""proyectoEmat URL Configuration

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
from users import views
from django.conf.urls import handler404
from core import views as core_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ggalbas/', include('ggalbas.urls')),
    path('ggtutbas/', include('ggtutbas.urls')),
    path('logout', views.logout),
    path('verificaSession', views.verificaSession),
    path('visores/', include('visores.urls')),
    path('visortut/', include('visorA2Tutor.urls')),
]

handler404 = core_views.handler404
handler500 = core_views.handler500
