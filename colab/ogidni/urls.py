from django.conf.urls import patterns, url
from ogidni import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_story/$', views.add_story, name='add_story'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^(?P<genre_name_url>\w+)/$', views.genre, name='genre'),
        url(r'^(?P<genre_name_url>\w+)/(?P<story_name_url>\w+)/$', views.story, name='story'),
        )
