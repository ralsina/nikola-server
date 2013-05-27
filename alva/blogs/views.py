from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from blogs.models import Blog, Post, Story
from blogs.forms import BlogForm, PostForm, StoryForm

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


# Blog CRUD

class BlogCreate(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('profile')


# Post CRUD

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('profile')

# Story CRUD

class StoryCreate(LoginRequiredMixin, CreateView):
    form_class = StoryForm
    model = Story
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(StoryCreate, self).form_valid(form)

class StoryUpdate(LoginRequiredMixin, UpdateView):
    form_class = StoryForm
    model = Story
    success_url = reverse_lazy('profile')

class StoryDelete(LoginRequiredMixin, DeleteView):
    model = Story
    success_url = reverse_lazy('profile')


# Special View for the profile|home

class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "blogs/profile.html"


