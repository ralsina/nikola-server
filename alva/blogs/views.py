from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response

from blogs.models import Blog, Post, Story
from blogs.forms import BlogForm, PostForm, StoryForm

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class OwnerOnlyMixin(LoginRequiredMixin):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.owner

    def get(self, request, *args, **kwargs):
        if not self.check_owner(request):
            raise PermissionDenied()
        return super(OwnerOnlyMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.check_owner(request):
            raise PermissionDenied()
        return super(OwnerOnlyMixin, self).post(request, *args, **kwargs)


# Blog CRUD

class BlogCreate(LoginRequiredMixin, CreateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BlogCreate, self).form_valid(form)

class BlogUpdate(OwnerOnlyMixin, UpdateView):
    form_class = BlogForm
    model = Blog
    success_url = reverse_lazy('profile')

class BlogDelete(OwnerOnlyMixin, DeleteView):
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

class PostUpdate(OwnerOnlyMixin, UpdateView):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.blog.owner or\
            request.user in self.object.blog.members.all()

    form_class = PostForm
    model = Post
    success_url = reverse_lazy('profile')

class PostDelete(OwnerOnlyMixin, DeleteView):

    def check_owner(self, request):
        self.object = self.get_object()
        return request.user==self.object.blog.owner or\
            request.user in self.object.blog.members.all()

    model = Post
    success_url = reverse_lazy('profile')

# Story CRUD

class StoryCreate(PostCreate):
    form_class = StoryForm
    model = Story

class StoryUpdate(PostUpdate):
    form_class = StoryForm
    model = Story

class StoryDelete(PostDelete):
    model = Story


# Special View for the profile|home

class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "blogs/profile.html"

import nikola.plugins.compile_rest
import nikola.plugins.compile_markdown
import nikola.plugins.compile_textile

def rest_preview(request):
    markup = nikola.plugins.compile_rest.rst2html(request.POST.get('data', ''))[0]
    return render_to_response( 'markitup/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))

def markdown_preview(request):
    markup = nikola.plugins.compile_markdown.markdown(request.POST.get('data', ''))
    print(repr(markup))
    return render_to_response( 'markitup/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))

def textile_preview(request):
    markup = nikola.plugins.compile_textile.textile(request.POST.get('data', ''))
    return render_to_response( 'markitup/preview.html',
                              {'preview': markup},
                              context_instance=RequestContext(request))

