from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    like_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts', blank=True)
    updated_at=models.DateTimeField(null=True, blank=True, auto_now=True)
    
    def __str__(self):
        return self.title
    
    # def count_likes_user(self):
    #     return self.like_users.count()

class Image(models.Model):
    post=models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    image=models.ImageField(blank=True, upload_to="images/")
    
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    writer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment