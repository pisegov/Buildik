from django.urls import path, re_path
from pccomponents import admin_views
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
    re_path(f'^category-(?P<category>{CATEGORIES})/$', admin_views.ItemList.as_view()),
    re_path(f'^category-(?P<category>{CATEGORIES})/(?P<pk>[0-9]+)/$', admin_views.ItemDetail.as_view()),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS})/$', admin_views.SpecificationList.as_view()),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS})/(?P<pk>[0-9]+)/$', admin_views.SpecificationDetail.as_view()),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS})/$', admin_views.BelongingList.as_view()),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS})/(?P<pk>[0-9]+)/$', admin_views.BelongingDetail.as_view()),
]