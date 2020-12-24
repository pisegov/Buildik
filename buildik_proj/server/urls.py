"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import logout, views as auth_views
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from server import views


mainurlpatterns = [
    path("home/", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),

    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),

    path('api/pccomponents/', include('pccomponents.urls')),
    path('api/admin/pccomponents/', include('pccomponents.admin_urls')),
    path('api/setups/', include('setups.urls')),
    path('api/user/', include('users.urls')),
]

schema_view = get_swagger_view(title='Buildik API', patterns=mainurlpatterns)

urlpatterns = mainurlpatterns + [
    path('api/docs/', schema_view),
    # path('', views.index)
]
