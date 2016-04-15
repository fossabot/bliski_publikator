# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MonitoringListView.as_view(),
        name="list"),
    url(r'^~create$', views.MonitoringCreateView.as_view(),
        name="create"),
    url(r'^monitoring-autocomplete$', views.MonitoringAutocomplete.as_view(),
        name="autocomplete"),
    url(r'^monitoring-(?P<slug>[\w-]+)$', views.MonitoringDetailView.as_view(),
        name="details"),
    url(r'^monitoring-(?P<slug>[\w-]+)/~update$', views.MonitoringUpdateView.as_view(),
        name="update"),
    url(r'^monitoring-(?P<slug>[\w-]+)/~delete$', views.MonitoringDeleteView.as_view(),
        name="delete"),
]
