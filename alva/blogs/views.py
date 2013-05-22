from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

class LoginRequired(object):
    """Mixin for view classes that require a user."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

class ProfileView(TemplateView, LoginRequired):

    template_name = "blogs/profile.html"

