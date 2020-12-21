from django.urls import path, re_path
from pccomponents import admin_views
import pccomponents.models as pcc
from pccomponents.config import CATEGORIES_REGEX, SPECIFICATIONS_REGEX, BELONGINGS_REGEX


urlpatterns = [
    re_path(f'^category-(?P<category>{CATEGORIES_REGEX})/$', admin_views.ItemList.as_view()),
    re_path(f'^category-(?P<category>{CATEGORIES_REGEX})/(?P<pk>[0-9]+)/$', admin_views.ItemDetail.as_view()),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS_REGEX})/$', admin_views.SpecificationList.as_view()),
    re_path(f'^specification-(?P<specification>{SPECIFICATIONS_REGEX})/(?P<pk>[0-9]+)/$', admin_views.SpecificationDetail.as_view()),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS_REGEX})/$', admin_views.BelongingList.as_view()),
    re_path(f'^belonging-(?P<belonging>{BELONGINGS_REGEX})/(?P<pk>[0-9]+)/$', admin_views.BelongingDetail.as_view()),
]