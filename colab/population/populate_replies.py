from random_paragraph import random_paragraphs

import os
import sys
import random
import datetime

def populate_reply():
    dates_short = [datetime.datetime.now() - datetime.timedelta(days=x, hours=y, minutes=z)
            for x in range(3) for y in range(25) for z in range(61)]

    user_objects = [user for user in User.objects.all()] # list of user objects
    story_objects = [story for story in Story.objects.all()] # list of story objects

    reply_objects = []
    for story in story_objects[:100]: # limit replies to first 100 stories
        replies = [reply for x in range(2) for reply in random_paragraphs(0.08)]

        for reply in replies:
            reply_objects.append(add_reply(random.choice(user_objects), story, reply, random.choice(dates_short), None))

        for reply in reply_objects:
            add_reply(random.choice(user_objects), reply.story, random.choice(replies), random.choice(dates_short), reply) # replies to replies


def add_reply(user, story, text, postdate, parent=None, upvotes=0, downvotes=0):
    r = Reply.objects.get_or_create(user=user, story=story, text=text, parent=parent,
            upvotes=random.randrange(1000), downvotes=random.randrange(1000), postdate=postdate)[0]

    return r

if __name__ == '__main__':
    sys.path.append("..")   # allow import from parent folder
    print 'Populating Replies'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')
    from django.contrib.auth.models import User
    from ogidni.models import Story, Reply
    populate_reply()
