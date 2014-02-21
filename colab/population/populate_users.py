import os
import sys
import string
import random


def password_generator(size=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))


def populate_user():
    usernames = open("usernames").readlines()
    passwords = [password_generator() for i in range(len(usernames))]
    emails = [user.replace('\n', '') + "@gmail.com" for user in usernames]

    for user, password, email in zip(usernames, passwords, emails):
        add_user(user.replace('\n', ''), password, email)


def add_user(username, password, email):
    User.objects.get_or_create(username=username,
                               password=password, email=email)[0]

if __name__ == '__main__':
    sys.path.append("..")   # allow import from parent folder
    print 'Populating Users'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')
    from django.contrib.auth.models import User
    populate_user()
