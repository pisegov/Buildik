from django.urls import path
from django.conf.urls import url
import users.views as views

urlpatterns = [
    path('', views.show_user),
    url(r'^update/$', views.update_user, name='update'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^signup/$', views.user_signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    path('delete/', views.delete_user),
]
