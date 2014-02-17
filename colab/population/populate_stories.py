from random_titles import random_titles
from random_paragraph import random_paragraphs

import os
import sys
import random
import datetime

def populate_story():
    dates = [datetime.datetime.now() - datetime.timedelta(days=x, hours=y, minutes=z) \
            for x in range(60) for y in range(25) for z in range(61)]
    dates_short = [datetime.datetime.now() - datetime.timedelta(days=x, hours=y, minutes=z) \
            for x in range(3) for y in range(25) for z in range(61)]

    genre_objects = [genre for genre in Genre.objects.all()] # list of genre objects
    user_objects = [user for user in UserProfile.objects.all()] # list of user objects
    story_titles = [title for x in range(50) for title in random_titles()] # generates list of ~300 titles
    stories = [story for x in range(33) for story in random_paragraphs(0.1)] # generate list of ~297 paragraphs
    
    for title, text, genre, user, postdate in zip(story_titles, stories, \
            [g for i in range(len(genre_objects)) for g in genre_objects], user_objects, dates):
        add_story(title, text, genre, user, postdate) # genre list comprehension generates list of len of ~287

def add_story(name, text, genre, author, postdate, upvotes=0, downvotes=0):
    s = Story.objects.get_or_create(name=name, text=text, genre=genre, author=author, url=name.replace(' ', '_').lower(),
            upvotes=random.randrange(1000), downvotes=random.randrange(1000), postdate=postdate)[0]

if __name__ == '__main__':
    sys.path.append("..")   # allow import from parent folder
    print 'Populating Stories'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')
    from ogidni.models import Genre, UserProfile, Story
    populate_story()
