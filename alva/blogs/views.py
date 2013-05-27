from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from blogs.models import Blog, Post, Story
from blogs.forms import BlogForm, PostForm, StoryForm

# Blog CRUD

class BlogCreate(CreateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(UpdateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

class BlogDelete(DeleteView):
    model = Blog
    success_url = reverse_lazy('profile')


# Post CRUD

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('profile')

# Story CRUD

class StoryCreate(CreateView):
    form_class = StoryForm
    model = Story
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(StoryCreate, self).form_valid(form)

class StoryUpdate(UpdateView):
    form_class = StoryForm
    model = Story
    success_url = reverse_lazy('profile')

class StoryDelete(DeleteView):
    model = Story
    success_url = reverse_lazy('profile')


# Special View for the profile|home

class ProfileView(TemplateView):

    template_name = "blogs/profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

