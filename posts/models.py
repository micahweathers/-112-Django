from django.db import models
from django.contrib.auth import get_user_model

# Status model MUST come before Post model!
class Status(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(
        max_length=256,
        help_text="Write a description about the status"
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Status"


class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)  # NEW!
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"