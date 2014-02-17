from bs4 import BeautifulSoup
import requests
from time import sleep

def random_paragraphs(request_wait=0):
    """ Returns ~9 paragraphs of text in a list.
        request_wait is for recursive calls to prevent denial-of-service like effects. """

    url = "http://randomtextgenerator.com/"
    payload = {'text_mode': 'html', 'language': 'en', 'Go': 'Go'}

    session = requests.session()
    r = requests.post(url, data=payload)

    data = r.text
    soup = BeautifulSoup(data)

    paragraph = [p.getText() for p in soup.find_all('p')]

    sleep(request_wait)

    return paragraph

