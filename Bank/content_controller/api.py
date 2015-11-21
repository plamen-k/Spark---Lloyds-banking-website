# Code written by Plamen Kolev

from django.http import HttpResponse
from django.core import serializers
from .models import UserStory
import json

def getUserStories(request):
	userStories = serializers.serialize("json", UserStory.objects.all())
	return HttpResponse(json.dumps(userStories), content_type='application/json')