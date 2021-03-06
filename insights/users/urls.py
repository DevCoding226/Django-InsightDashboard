# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/?$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/change/?$',
        view=views.UserUpdateView.as_view(),
        name='update_user'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/set_password/?$',
        view=views.UserSetPasswordView.as_view(),
        name='set_password'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/detele/?$',
        view=views.DeleteUser.as_view(),
        name='delete_user'
    ),
    url(
        regex=r'^~create/?$',
        view=views.UserCreateView.as_view(),
        name='create_user'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^(?P<hash>.*)/complete_signup/?$',
        view=views.CompleteSignupView.as_view(),
        name='complete'
    ),
]
