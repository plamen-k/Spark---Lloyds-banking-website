# Code written by Plamen Kolev

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from content_controller.models import Service, UserStory
from Bank.views import baseDict

def service(request, slug=None):
    dictionary = baseDict(request)
    service = Service.objects.get(slug=slug)

    dictionary.update({
        'service' : service,
    })
    return render_to_response("controller/service.html", dictionary)

def story(request, slug=None):
    dictionary = baseDict(request)
    story = UserStory.objects.get(slug=slug)

    dictionary.update({
        'story' : story,
    })

    return render_to_response("controller/story.html", dictionary)
