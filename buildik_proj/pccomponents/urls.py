from django.urls import path, re_path
from pccomponents import views
import pccomponents.models as pcc

CATEGORIES = ''
for t in pcc.ITEMS:
    CATEGORIES += t[1] + '|'
CATEGORIES = CATEGORIES[:-1]

SPECIFICATIONS = ''
for s in pcc.SPECIFICATIONS:
    SPECIFICATIONS += s + '|'
SPECIFICATIONS = SPECIFICATIONS[:-1]

BELONGINGS = ''
for s in pcc.BELONGINGS:
    BELONGINGS += s + '|'
BELONGINGS = BELONGINGS[:-1]

urlpatterns = [
    path('', views.get_all_pccomponents),
    path('<int:pk>/', views.get_pccomponent),
    re_path(f'^category-(?P<category>{CATEGORIES})/$', views.get_category),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS})/$', views.get_specification),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS})/$', views.get_belonging),
]