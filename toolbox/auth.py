"""Decorators for the authentication framework."""

from django.conf import settings
from google.appengine.api import users
from django.http import Http404, HttpResponseRedirect


def admin_required(function):
  """
    Rough implementation of Django's staff_member decorator.

    Throw an 404 if the request is made by a user whose email is
    not listed in the settings.py ADMIN list.
  """
  def admin_required_wrapper(request, *args, **kw):
    ADMIN_EMAILS= [i[1] for i in settings.ADMINS]
    if getattr(request.user, 'email', None) in ADMIN_EMAILS:
      return function(request, *args, **kw)
    return HttpResponseRedirect(users.create_login_url(request.path))
  return admin_required_wrapper

