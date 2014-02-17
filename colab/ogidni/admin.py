from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ogidni.models import Story, UserProfile, Genre, Reply, Vote

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'genre', 'author', 'url', 'upvotes', 'downvotes', 'postdate')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'story', 'preply', 'text', 'upvotes', \
            'downvotes')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'reply', 'direction')

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'date_joined', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Vote, VoteAdmin)

