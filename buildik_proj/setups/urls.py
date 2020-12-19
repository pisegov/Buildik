from django.urls import path
from setups import views

urlpatterns = [
    path('', views.SetupList.as_view()),
    path('<int:pk>/', views.SetupDetail.as_view()),
    path('items/', views.SetupItemList.as_view()),
    path('items/<int:pk>/', views.SetupItemDetail.as_view()),
    path('apicheck/', views.api_check)
]