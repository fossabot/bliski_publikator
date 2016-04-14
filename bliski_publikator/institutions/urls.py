# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.InstitutionListView.as_view(),
        name="list"),
    url(r'^~create$', views.InstitutionCreateView.as_view(),
        name="create"),
    url(r'^institution-(?P<slug>[\w-]+)$', views.InstitutionDetailView.as_view(),
        name="details"),
    url(r'^institution-(?P<slug>[\w-]+)/~update$', views.InstitutionUpdateView.as_view(),
        name="update"),
    url(r'^institution-(?P<slug>[\w-]+)/~delete$', views.InstitutionDeleteView.as_view(),
        name="delete"),
]
