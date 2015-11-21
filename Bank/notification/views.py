# Code written by Plamen Kolev

from django.shortcuts import render, render_to_response
from notification.models import Notification
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Bank.views import baseDict

@login_required
def markRead(request, pk):
	Notification.objects.get(pk=pk, to=request.user).markRead()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def markAllRead(request):
	Notification.objects.get(pk=0, to=request.user).markAllRead(request.user)

@login_required
def all(request):
	myDict = baseDict(request)
	myDict.update({
		'messages' : Notification.objects.filter(to=request.user).order_by("-theDate")
	})
	return render_to_response("notification/messages.html", myDict)

@login_required
def fullMessage(request,pk):
	myDict = baseDict(request)
	singleMessage = Notification.objects.get(pk=pk, to=request.user)
	singleMessage.read = True
	singleMessage.save()
	myDict.update({
		'message' : singleMessage
	})
	return render_to_response("notification/fullview.html", myDict)

def fullMassMessage(request, pk):
	return HttpResponse("hello world")