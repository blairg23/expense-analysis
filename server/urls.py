"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import re_path, path
from rest_framework.routers import DefaultRouter

from expensive.urls import expensive_api_router

api_root_router = DefaultRouter()
api_root_router.registry.extend(expensive_api_router.registry)

app_name = 'server'

urlpatterns = [
	#
	# Administration
	#
	# url(r'^admin_tools/', include('admin_tools.urls')),
    re_path(r'^admin/', admin.site.urls),
    #
    # Authentication
    #
    re_path(r'^api/auth/', include('rest_auth.urls')),
    #
    # Registration
    #
    re_path(r'^api/auth/register/', include('rest_auth.registration.urls')),
    #
    # API Docs
    #
    re_path(r'^api/docs/', include('rest_framework_docs.urls')),
    #
    # API
    #
    re_path(r'^api/', include((api_root_router.urls, "api"), namespace="api")),
]
