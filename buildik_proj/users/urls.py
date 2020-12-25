from django.urls import path
from django.conf.urls import url
import users.views as views

urlpatterns = [
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    path('delete/', views.delete_user),
]
