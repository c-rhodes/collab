from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ogidni.models import Story, UserProfile, Genre, Reply, StoryLike, StoryDislike, ReplyLike, ReplyDislike

class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'genre', 'author', 'url', 'upvotes', 'downvotes', 'postdate')

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'story', 'parent', 'text', 'upvotes', \
            'downvotes')

class StoryLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'story')

class StoryDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'story')

class ReplyLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'reply')

class ReplyDislikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'reply')

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'date_joined', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(StoryLike, StoryLikeAdmin)
admin.site.register(StoryDislike, StoryDislikeAdmin)
admin.site.register(ReplyLike, ReplyLikeAdmin)
admin.site.register(ReplyDislike, ReplyDislikeAdmin)

