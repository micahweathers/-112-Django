from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]