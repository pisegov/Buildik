from django.urls import path, re_path
from pccomponents import views
import pccomponents.models as pcc
from pccomponents.config import CATEGORIES_REGEX, SPECIFICATIONS_REGEX, BELONGINGS_REGEX


urlpatterns = [
    path('', views.get_all_pccomponents),
    path('<int:pk>/', views.get_pccomponent),
    re_path(f'^category-(?P<category>{CATEGORIES_REGEX})/$', views.get_category),
    re_path(f'^category-(?P<category>{CATEGORIES_REGEX})/setup-(?P<pk>[0-9]+)/$', views.get_category_for_setup),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS_REGEX})/$', views.get_specification),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS_REGEX})/$', views.get_belonging),
]