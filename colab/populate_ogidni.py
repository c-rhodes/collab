from datetime import datetime

import os
import random
import string

def password_generator(size=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))

def populate():
    genres = ['Adventure',
            'American Literature',
            'Biography',
            'Classics',
            'Computing',
            'Crime Fiction',
            'Cyberpunk',
            'Fantasy',
            'Fiction',
            'History',
            'Horror',
            'Philosophy',
            'Poetry',
            'Politics',
            'Sci-fi',
            'Science Fiction',
            'War']
    
    genre_objects = [add_genre(genre.lower()) for genre in genres]
    
    users = ['Cullen', 'Chris', 'Adam', 'Wes', 'Steven', 'David', 'Darren',
            'Michael', 'Hannah', 'Alex', 'Becky', 'Lyla', 'Ayn', 'Abbie',
            'Laura', 'Chukwuddi', 'Luke']
    passwords = [password_generator() for i in range(len(users))]
    emails = [(user+"@gmail.com") for user in users]

    user_objects = []
    for user, password, email in zip(users, passwords, emails):
        user_objects.append(add_user(user, password, email))

    story_names = [s for s in os.listdir("stories")]
    stories = [open("stories/"+s).read() for s in story_names]

    story_objects = []
    for story_name, story, genre, user in zip(story_names, stories, genre_objects, user_objects):
        story_objects.append(add_story(story_name, story, genre, user))

def add_genre(genre):
    g = Genre.objects.get_or_create(name=genre)[0]
    return g

def add_user(username, password, email):
    u = User.objects.get_or_create(username=username,
            password=password, email=email)[0]
    up = UserProfile.objects.get_or_create(picture=None, user=u)[0]
    return up

def add_story(name, text, genre, author, upvotes=0, downvotes=0):
    s = Story.objects.get_or_create(name=name, text=text, genre=genre, author=author,
            upvotes=random.randrange(1000), downvotes=random.randrange(1000), postdate=datetime.now())[0]
    return s

def add_reply(user_id, story_id, parent, text, upvotes=0, downvotes=0, postdate=0):
    r = Replies.objects.get_or_create(user_id=user_id, story_id=story_id, parent=parent, text=text, upvotes=random.randrange(1000), downvotes=random.randrange(1000))[0]
    return r

if __name__ == '__main__':
    print 'Populating Ogidni with filthy datas. absolutely filthy stuff'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')
    from ogidni.models import Genre, UserProfile, User, Story, Replies
    populate()
