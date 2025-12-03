from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Status
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/new.html'
    fields = ['title', 'subtitle', 'body', 'image']  # Removed status - will be set by button
    
    def form_valid(self, form):
        form.instance.author = self.request.user  # Auto-set logged-in user as author
        
        # Check which button was clicked
        if 'save_draft' in self.request.POST:
            # Get or create Draft status
            draft_status, created = Status.objects.get_or_create(
                name='Draft',
                defaults={'description': 'Posts visible only to the author'}
            )
            form.instance.status = draft_status
        elif 'publish' in self.request.POST:
            # Get or create Published status
            published_status, created = Status.objects.get_or_create(
                name='Published',
                defaults={'description': 'Posts available for all to view'}
            )
            form.instance.status = published_status
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    fields = ['title', 'subtitle', 'body', 'image']  # Removed status - will be set by button
    
    def form_valid(self, form):
        # Check which button was clicked
        if 'save_draft' in self.request.POST:
            draft_status, created = Status.objects.get_or_create(
                name='Draft',
                defaults={'description': 'Posts visible only to the author'}
            )
            form.instance.status = draft_status
        elif 'publish' in self.request.POST:
            published_status, created = Status.objects.get_or_create(
                name='Published',
                defaults={'description': 'Posts available for all to view'}
            )
            form.instance.status = published_status
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'
    success_url = reverse_lazy('posts:list')