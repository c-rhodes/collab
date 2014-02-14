from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from ogidni.models import Story, Genre, Replies
from ogidni.sorts import confidence, hot

from ogidni.forms import StoryForm, UserForm, UserProfileForm

from datetime import datetime
from reportlab.pdfgen import canvas

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('ogidni/register.html',
            {'user_form': user_form, 'profile_form': profile_form,
                'registered': registered}, context)

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
            story.save()
            posted = True
        else:
            print form.errors
    else:
        form = StoryForm

    return render_to_response('ogidni/add_story.html',
            {'form': form,
                'posted': posted,
                }, context)

def index(request):
    context = RequestContext(request)
    story_list = Story.objects.order_by('-upvotes')

    stories = sorted(Story.objects.all(), key=lambda Story: -hot(Story.upvotes, Story.downvotes, datetime.now()))

    for story in stories:
        s_confidence = confidence(story.upvotes, story.downvotes)
        print story, s_confidence

    for story in stories:
        genre_name = Genre.objects.get(name=story.genre)
        story.url = story_url_encode(genre_name.name+'/'+story.name)

    story_dict = {'stories': stories}
    response = render_to_response('ogidni/index.html', story_dict, context)

    visits = int(request.COOKIES.get('visits', '0'))

    if request.COOKIES.has_key('last_visit'):
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

    genre_name = story_url_decode(genre_name_url)
    context_dict = {'genre_name': genre_name}
    
    try:
        genre = Genre.objects.get(name=genre_name)
        pages = Story.objects.filter(genre=genre.id)
        context_dict['pages'] = pages
        context_dict['genre'] = genre
        for page in pages:
            page.url = story_url_encode(page.name)
    except Genre.DoesNotExist:
        pass


    return render_to_response('ogidni/genre.html', context_dict, context)

def story(request, genre_name_url, story_name_url):
    context = RequestContext(request)

    genre_name = story_url_decode(genre_name_url)
    story_name = story_url_decode(story_name_url)
    context_dict = {'story_name': story_name}

    try:    
        story = Story.objects.get(name=story_name)
        story.url = story_url_encode(genre_name+'/'+story_name)
        context_dict['story'] = story
    except Story.DoesNotExist:
        pass

    try:
        replies = sorted(Replies.objects.filter(story=story.id), key=lambda Replies: -confidence(Replies.upvotes, Replies.downvotes))
        context_dict['replies'] = replies
    except Replies.DoesNotExist:
        pass

    return render_to_response('ogidni/story.html', context_dict, context)

def generate_pdf(request, genre_name_url, story_name_url):
    genre_name = story_url_decode(genre_name_url)
    story_name = story_url_decode(story_name_url)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + story_name_url + '.pdf'
    
    p = canvas.Canvas(response)
    p.drawString(100, 100, "Hello world.")

    p.showPage()
    p.save()
    return response


def story_url_encode(story_name_url):
    return story_name_url.replace(' ', '_')

def story_url_decode(story_name):
    return story_name.replace('_', ' ')

