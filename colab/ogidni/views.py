from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import serializers

from ogidni.models import Story, Genre, Reply, Vote
from ogidni.sorts import confidence, hot
from ogidni.forms import StoryForm, UserForm

from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas

import json
import urllib


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response('ogidni/register.html', {
                              'user_form': user_form,
                              'registered': registered}, context)


def vote(request):

    if request.method == 'GET':
        parent = int(request.GET['par'])
        object_id = int(request.GET['object_id'])
        direction = int(request.GET['dir'])
    else:
        return HttpResponse(status=400)

    if request.user.is_authenticated():
        upvotes = 0
        downvotes = 0
        if object_id:
            if parent is 1:
                story_object = Story.objects.get(id=int(object_id))

                try:
                    # opposite of registered vote already exists
                    vote_exists = Vote.objects.get(user=request.user,
                            story=story_object, direction=not direction)
                    if story_object:
                        if direction is 1:
                            upvotes = story_object.upvotes + 1
                            story_object.upvotes = upvotes
                            downvotes = story_object.downvotes - 1
                            story_object.downvotes = downvotes
                        elif direction is 0:
                            downvotes = story_object.downvotes + 1
                            story_object.downvotes = downvotes
                            upvotes = story_object.upvotes - 1
                            story_object.upvotes = upvotes
                        else:
                            return HttpResponse(status=400)
                        
                        vote_created = Vote.objects.create(user=request.user,
                            story=story_object, direction=direction)

                        vote_exists.delete()
                        story_object.save()
                    
                except Vote.DoesNotExist:
                    vote_created = Vote.objects.get_or_create(user=request.user,
                            story=story_object, direction=direction)
                    
                    if not vote_created[1]:
                        # vote already exists so undo original vote
                        if story_object:
                            if direction is 1:
                                upvotes = story_object.upvotes - 1 # remove upvote
                                story_object.upvotes = upvotes
                                downvotes = story_object.downvotes
                            elif direction is 0:
                                downvotes = story_object.downvotes - 1  # remove downvote
                                story_object.downvotes = downvotes
                                upvotes = story_object.upvotes
                            else:
                                return HttpResponse(status=400)
        
                        # cleanup: remove vote object that already exists
                        Vote.objects.get(user=request.user, story=story_object,
                                direction=direction).delete()
                        story_object.save()
                    else:
                        if story_object:
                            if direction is 1:
                                upvotes = story_object.upvotes + 1
                                story_object.upvotes = upvotes
                                downvotes = story_object.downvotes
                            elif direction is 0:
                                downvotes = story_object.downvotes + 1
                                story_object.downvotes = downvotes
                                upvotes = story_object.upvotes
                            else:
                                return HttpResponse(status=400)
                        story_object.save()
            elif parent is 2:
                # vote on a reply
                reply_object = Reply.objects.get(id=int(object_id))

                try:
                    # opposite of registered vote already exists
                    vote_exists = Vote.objects.get(user=request.user,
                            reply=reply_object, direction=not direction)
                    if reply_object:
                        if direction is 1:
                            upvotes = reply_object.upvotes + 1
                            reply_object.upvotes = upvotes
                            downvotes = reply_object.downvotes - 1
                            reply_object.downvotes = downvotes
                        elif direction is 0:
                            downvotes = reply_object.downvotes + 1
                            reply_object.downvotes = downvotes
                            upvotes = reply_object.upvotes - 1
                            reply_object.upvotes = upvotes
                        else:
                            return HttpResponse(status=400)
                        
                        vote_created = Vote.objects.create(user=request.user,
                            reply=reply_object, direction=direction)

                        vote_exists.delete()
                        reply_object.save()
                    
                except Vote.DoesNotExist:
                    vote_created = Vote.objects.get_or_create(user=request.user,
                            reply=reply_object, direction=direction)
                    
                    if not vote_created[1]:
                        # vote already exists so undo original vote
                        if reply_object:
                            if direction is 1:
                                upvotes = reply_object.upvotes - 1 # remove upvote
                                reply_object.upvotes = upvotes
                                downvotes = reply_object.downvotes
                            elif direction is 0:
                                downvotes = reply_object.downvotes - 1  # remove downvote
                                reply_object.downvotes = downvotes
                                upvotes = reply_object.upvotes
                            else:
                                return HttpResponse(status=400)
        
                        # cleanup: remove vote object that already exists
                        Vote.objects.get(user=request.user, reply=reply_object,
                                direction=direction).delete()
                        reply_object.save()
                    else:
                        if reply_object:
                            if direction is 1:
                                upvotes = reply_object.upvotes + 1
                                reply_object.upvotes = upvotes
                                downvotes = reply_object.downvotes
                            elif direction is 0:
                                downvotes = reply_object.downvotes + 1
                                reply_object.downvotes = downvotes
                                upvotes = reply_object.upvotes
                            else:
                                return HttpResponse(status=400)
                        reply_object.save()
                    
            else:
                # parent unknown
                return HttpResponse(status=500)

            response_data = {'loggedIn': True, 'votes':
                            {'upvotes': upvotes, 'downvotes': downvotes}}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            # no object_id 
            return HttpResponse(status=500)
    else:
        # user not authenticated
        response_data = {'loggedIn': False, 'votes':
                        {'upvotes': 0, 'downvotes': 0}}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def reply(request):

    if request.method == 'GET':
        story_id = int(request.GET['story_id'])
        reply_id = int(request.GET['reply_id'])
        editor_data = request.GET['editor_data']
    else:
        return HttpResponse(status=400)

    if request.user.is_authenticated():
        if story_id and reply_id is not None:
            req_user = User.objects.get(username=request.user)
            story_object = Story.objects.get(id=int(story_id))
            if reply_id is not 0:
                reply_object = Reply.objects.get(id=int(reply_id))
            else:
                reply_object = None

            text_data = urllib.unquote(str(editor_data)).decode("utf-8")
            new_reply = Reply(user=req_user, story=story_object,
                              parent=reply_object, text=text_data, postdate=datetime.now())
            new_reply.save()

            reply_json = serializers.serialize("json", new_reply)
            response_data = {'loggedIn': True, 'posted': True, 'new_object': reply_json}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(status=400)
    else:
        response_data = {'loggedIn': False, 'posted': False}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def user_overview(request, username):
    context = RequestContext(request)

    user_exists(username)

    stories = Story.objects.filter(author__username__iexact=username).order_by('-postdate')
    for story in stories:
        story.url = story.genre.url + '/' + story.url

    context_dict = {'stories': stories}

    return render_to_response('ogidni/user_overview.html', context_dict, context)


def user_comments(request, username):
    context = RequestContext(request)

    user_exists(username)

    replies = Reply.objects.filter(user__username__iexact=username).order_by('-postdate')
    for reply in replies:
        reply.url = reply.story.genre.url + '/' + reply.story.url

    context_dict = {'replies': replies}

    return render_to_response('ogidni/user_comments.html', context_dict, context)


def user_liked(request, username):
    context = RequestContext(request)

    user_exists(username)

    likes = Vote.objects.filter(user__username__iexact=username, reply=None, direction=True)
    for like in likes:
        like.url = like.story.genre.url + '/' + like.story.url

    context_dict = {'likes': likes}

    return render_to_response('ogidni/user_liked.html', context_dict, context)


def user_disliked(request, username):
    context = RequestContext(request)

    user_exists(username)

    dislikes = Vote.objects.filter(user__username__iexact=username, reply=None, direction=False)

    for dislike in dislikes:
        dislike.url = dislike.story.genre.url + '/' + dislike.story.url

    context_dict = {'dislikes': dislikes}

    return render_to_response('ogidni/user_disliked.html', context_dict, context)


def user_exists(username):
    """ Determines is user exists, raising 404 error if not. """
    try:
        User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ogidni')
            else:
                return HttpResponse('Your account has been disabled')
        else:
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse("Invalid login details")
    else:
        return render_to_response('ogidni/login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/ogidni/')


@login_required
def add_story(request):
    context = RequestContext(request)
    posted = False

    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.author_id = request.user.id
            print "user id: " + str(request.user.id)
            print "story id: " + str(story.author_id)
            story.postdate = datetime.now()
            story.url = request.POST['name'].replace(' ', '_').lower()
            story.save()
            posted = True
        else:
            print form.errors
    else:
        form = StoryForm

    return render_to_response('ogidni/add_story.html',
                              {'form': form, 'posted': posted, }, context)


def index(request):
    context = RequestContext(request)

    stories = sorted(Story.objects.all(), key=lambda Story: -hot(Story.upvotes,
                     Story.downvotes, datetime.now()))[:20]  # limit by 20

    try:
        for story in stories:
            genre = Genre.objects.get(name=story.genre)
            story.url = genre.url + '/' + story.url

        story_dict = {'stories': stories}
    except Genre.DoesNotExist:
        pass

    response = render_to_response('ogidni/index.html', story_dict, context)

    visits = int(request.COOKIES.get('visits', '0'))

    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if(datetime.now() - last_visit_time).days > 5:
            response.set_cookie('visits', visits+1)
            response.set_cookie('last_visit', datetime.now())
    else:
        response.set_cookie('last_visit', datetime.now())

    return response


def genre(request, genre_name_url):
    context = RequestContext(request)
    context_dict = {}

    try:
        genre = Genre.objects.get(url__iexact=genre_name_url)
        pages = Story.objects.filter(genre=genre.id)
        context_dict = {'genre': genre}
        context_dict['pages'] = pages
    except (Genre.DoesNotExist, Story.DoesNotExist):
        raise Http404

    return render_to_response('ogidni/genre.html', context_dict, context)


def story(request, genre_name_url, story_name_url):
    context = RequestContext(request)
    context_dict = {}

    try:
        genre = Genre.objects.get(url__iexact=genre_name_url)
        story = Story.objects.get(url__iexact=story_name_url)
        context_dict = {'story': story}
        story.url = genre.url+'/'+story.url
        replies = sorted(Reply.objects.filter(story=story.id),
                         key=lambda Reply: -confidence(Reply.upvotes, Reply.downvotes))
        context_dict['replies'] = replies
    except (Genre.DoesNotExist, Story.DoesNotExist, Reply.DoesNotExist):
        raise Http404

    return render_to_response('ogidni/story.html', context_dict, context)


def generate_pdf(request, genre_name_url, story_name_url):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + story_name_url + '.pdf'

    buffer = BytesIO()
    
    p = canvas.Canvas(buffer)

    try:    
        genre = Genre.objects.get(url=genre_name_url)
        story = Story.objects.get(url=story_name_url)
        story.url = genre_url+'/'+story.url
        replies = sorted(Reply.objects.filter(story=story.id), key=lambda Reply: -confidence(Reply.upvotes, Reply.downvotes))
    except (Genre.DoesNotExist, Story.DoesNotExist, Reply.DoesNotExist):
        pass

    p.drawString(100, 750, story.text)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
