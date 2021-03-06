# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64

from allauth.account.forms import SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import TimestampSigner, SignatureExpired
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.views.generic import (
    DetailView, ListView, RedirectView, UpdateView,
    CreateView, FormView, DeleteView
)
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.contrib import messages

from .models import User
from .forms import UpdateUserForm, CreateUserForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    permission_required = 'users.change_user'
    raise_exception = True

    def get_success_url(self):
        return reverse('users:list')


class UserSetPasswordView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'account/password_change.html'
    permission_required = 'users.change_user'
    raise_exception = True

    def get_form(self, form_class=None):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return SetPasswordForm(self.user, **self.get_form_kwargs())

    def get_success_url(self):
        return reverse('users:update_user', kwargs={'username': self.kwargs['username']})

    def form_valid(self, form):
        # mark user as active if the password is set by admin
        self.user.is_active = True
        self.user.save()
        form.save()
        return super(UserSetPasswordView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return _('Password for %(username)s has been changed.') % {'username': self.user.name}


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.change_user'
    raise_exception = True
    slug_field = 'username'
    slug_url_kwarg = 'username'
    query_pk_and_slug = True
    success_url = reverse_lazy('users:list')


class DeleteUser(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'users.change_user'
    raise_exception = True
    slug_field = 'username'
    slug_url_kwarg = 'username'
    query_pk_and_slug = True
    success_url = reverse_lazy('users:list')


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = CreateUserForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    permission_required = 'users.change_user'
    raise_exception = True

    def get_success_url(self):
        return reverse('users:list')

    def form_valid(self, form):
        created_user = form.save()
        form.send_set_password_email(created_user, self.request)
        return HttpResponseRedirect(self.get_success_url())


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User

    slug_field = 'username'
    slug_url_kwarg = 'username'

    permission_required = 'users.change_user'
    raise_exception = True

    def get_queryset(self):
        qs = super().get_queryset().select_related("country").prefetch_related("therapeutic_areas", "groups")
        if not self.request.user.is_superuser:
            qs = qs.filter(is_superuser=False)
        return qs


class CompleteSignupView(FormView):
    form_class = SetPasswordForm
    template_name = 'users/set_initial_password.html'

    def _get_user_from_hash(self, hash):
        signer = TimestampSigner()
        decoded_hash = base64.urlsafe_b64decode(hash)
        max_age = settings.NEW_PASSWORD_TIMEOUT_DAYS * 24 * 60 * 60
        try:
            email = signer.unsign(decoded_hash, max_age=max_age)
        except SignatureExpired:
            messages.warning(
                self.request,
                _("Your link has expired. Please request a new one."))
            return None

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(
                self.request,
                _("The e-mail address is not assigned to any user account: {email}").format(email=email))
            return None

        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        # If form is valid, it means the user has successfully update his password,
        # so we can mark him as is_active so he can log in after redirect.
        self.user.is_active = True
        self.user.save()
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.user = self._get_user_from_hash(kwargs.get('hash'))
        if self.user is None:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
