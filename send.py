def vote(request):
    context = RequestContext(request)
    story_id = None
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
            if parent == 1:
                reply_object = Story.objects.get(id=int(object_id))
            elif parent == 2:
                reply_object = Reply.objects.get(id=int(object_id))
            else:
                return HttpResponse(status=400)

            if reply_object:
                if direction is 1:
                    upvotes = reply_object.upvotes + 1
                    reply_object.upvotes = upvotes
                    downvotes = reply_object.downvotes
                elif direction is 2:
                    downvotes = reply_object.downvotes + 1
                    reply_object.downvotes = downvotes
                    upvotes = reply_object.upvotes
                else:
                    return HttpResponse(status=400)

                reply_object.save()

                response_data = {'loggedIn':True, 'votes':{'upvotes': upvotes, 'downvotes': downvotes}}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=500)
    else:
        response_data = {'loggedIn':False, 'votes':{'upvotes': 0, 'downvotes': 0}}
        return HttpResponse(json.dumps(response_data), content_type="application/json")