from django.shortcuts import render

def list(request):
    """Display list of all posts"""
    return render(request, 'posts/list.html')

def detail(request, pk):
    """Display detail of a single post"""
    return render(request, 'posts/detail.html')

def new(request):
    """Create a new post"""
    return render(request, 'posts/new.html')

def delete(request, pk):
    """Delete a post"""
    return render(request, 'posts/delete.html')