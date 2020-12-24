from django.urls import path
import users.views as views

urlpatterns = [
    path('', views.get_user),
]