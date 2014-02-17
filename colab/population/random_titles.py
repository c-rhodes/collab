import math
import random

noun = open("nouns").readlines()
adjective = open("adjectives").readlines()

def random_titles():
    a = int(math.floor(random.random() * len(noun)))
    b = int(math.floor(random.random() * len(adjective)))
    title1 = (adjective[b] + " " + noun[a]).replace('\n', '')

    c = int(math.floor(random.random() * len(adjective)))
    d = int(math.floor(random.random() * len(noun)))
    title2 = ("The " + adjective[c] + " " + noun[d]).replace('\n', '')

    e = int(math.floor(random.random() * len(noun)))
    f = int(math.floor(random.random() * len(noun)))
    title3 = (noun[f] + " of " + noun[e]).replace('\n', '')

    g = int(math.floor(random.random() * len(noun)))
    h = int(math.floor(random.random() * len(noun)))
    title4 = ("The " + noun[g] + "'s " + noun[h]).replace('\n', '')

    i = int(math.floor(random.random() * len(noun)))
    j = int(math.floor(random.random() * len(noun)))
    title5 = ("The " + noun[i] + " of the " + noun[j]).replace('\n', '')

    k = int(math.floor(random.random() * len(noun)))
    l = int(math.floor(random.random() * len(noun)))
    title6 = (noun[k] + " in the " + noun[l]).replace('\n', '')
    
    return [title1, title2, title3, title4, title5, title6]
