from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('list/', views.PostListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostCreateView.as_view(), name='new'),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete'),
    path('comment/edit/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]