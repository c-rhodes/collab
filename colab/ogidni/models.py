from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Story(models.Model):
    name = models.CharField(max_length=64, unique=False)
    text = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(UserProfile,  on_delete=models.DO_NOTHING)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    postdate = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class Replies(models.Model):
    user = models.ForeignKey(UserProfile)
    story = models.ForeignKey(Story)
    parent = models.IntegerField(default=0)
    text = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.text

