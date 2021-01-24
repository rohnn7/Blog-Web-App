from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

# this class will contain all the information about the post
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #Builtin User table's userid is fk to Post Table
    title = models.CharField(max_length = 256)
    content = models.TextField()
    created_date = models.DateField(default = timezone.now)
    published_date = models.DateField(blank=True, null=True)

    #Here some functions would be there that would help handling db

    #will publish post DateField
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #will get a list of all approved comments
    def approve_comments(self):
        return self.comments.filter(is_approved=True)

    def __str__(self):
        return self.title

    #tells the post request what to do after a clicking btn
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk':self.pk})


#this class is of all comments done on every Post
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.CASCADE) #Postid(builtin by django) is fk to Comment table
    author = models.CharField(max_length=256)
    content = models.TextField()
    created_date = models.DateField(default=timezone.now())
    is_approved = models.BooleanField(default=False)

    #Here some functions would be there that would help handling db
    #will change the element is_approved from false to true
    def approve(self):
        self.is_approved = True
        self.save()

    def __str__(self):
        return self.author

    #tells the post request what to do after a clicking btn
    def get_absolute_url(self):
        return reverse('blog:post_list', kwargs={'pk':self.pk})
