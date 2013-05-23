from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from blogs.models import Blog
from blogs.forms import BlogForm

class BlogCreate(CreateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(UpdateView):
    model = Blog
    success_url = reverse_lazy('profile')

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('profile ')

class ProfileView(TemplateView):

    template_name = "blogs/profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

