from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=32, unique=True)
    url = models.TextField()
    
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
    postdate = models.DateTimeField()
    url = models.TextField() 

    def __unicode__(self):
        return self.name

class Reply(models.Model):
    user = models.ForeignKey(UserProfile)
    story = models.ForeignKey(Story, null=False)
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    text = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    postdate = models.DateTimeField()

    def __unicode__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(UserProfile, related_name='votes')
    story = models.ForeignKey(Story, related_name='votes', null=True, blank=True, default = None)
    reply = models.ForeignKey(Reply, related_name='votes', null=True, blank=True, default = None)
    direction = models.NullBooleanField(default=None)


