import os
import sys

def populate_genre():
    genres = open("genres").readlines()

    for genre in genres:
        add_genre(genre.replace('\n', ''))

def add_genre(genre):
    g = Genre.objects.get_or_create(name=genre, 
            url=genre.replace(' ', '_').lower())[0]

if __name__ == '__main__':
    sys.path.append("..")   # allow import from parent folder
    print 'Populating Genres'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colab.settings')
    from ogidni.models import Genre
    populate_genre()
