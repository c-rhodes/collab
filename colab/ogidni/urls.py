from django.conf.urls import patterns, url
from ogidni import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_story/$', views.add_story, name='add_story'),
        url(r'^vote/$', views.vote, name='vote'),
        url(r'^reply/$', views.reply, name='reply'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
        url(r'^user/(?P<username>\w+)/$', views.user_overview, name='user_overview'),
        url(r'^user/(?P<username>\w+)/liked/$', views.user_liked, name='user_liked'),
        url(r'^user/(?P<username>\w+)/disliked/$', views.user_disliked, name='user_disliked'),
        url(r'^user/(?P<username>\w+)/comments/$', views.user_comments, name='user_comments'),
        url(r'^(?P<genre_name_url>\w+)/$', views.genre, name='genre'),
        url(r'^(?P<genre_name_url>\w+)/(?P<story_name_url>\w+)/$', views.story, name='story'),
        url(r'^(?P<genre_name_url>\w+)/(?P<story_name_url>\w+)/pdf/$', views.generate_pdf, name='generate_pdf'),
        )
