def add_votes(user, story=None, reply=None, direction=None):
    v = Vote.objects.get_or_create(user=user, story=story, reply=reply, direction=random.choice([True, False]))[0]
    return v
