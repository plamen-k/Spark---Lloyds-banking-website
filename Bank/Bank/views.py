# Code written by Plamen Kolev

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.context_processors import csrf
from payment.models import BankingPerson, Account, OutgoingTransaction, IncomingTransaction
from notification.models import Notification
from content_controller.models import Slide, Service
from itertools import chain
from django.template import RequestContext


def index(request):

    if request.user.is_authenticated():
        dictData = baseDict(request)
    else:
        dictData = {}

    dictData.update({
        "slides" : Slide.objects.filter(display=True),
        'services' : Service.objects.filter(display=True),
    })
    return render_to_response("index.html", dictData, context_instance = RequestContext(request))

def testHtml(request):
    return render_to_response('test.html')

def baseDict(request): # this function allows you to extend dictionaries. The dict created by this function holds basic boilerplate info wich can be merget with a custom view dict
    c = {} # cross site protection token
    c.update(csrf(request))
    if request.user.is_authenticated():
        try:
            bankingP = BankingPerson.objects.get(user=request.user) # if so, fetch his banking person object
            accounts = bankingP.getAccounts() # all the accounts associated with him
            totalAmount = 0
            for acc in accounts:
                totalAmount += acc.amount # sum up the total money the person has
            user = request.user

            notViewednotifications =  Notification.objects.filter(to=request.user, viewed=False).order_by('-theDate')
            oldNotifications = Notification.objects.filter(to=request.user, viewed=True, read=False)[:10]

            notifications = chain(notViewednotifications, oldNotifications)


            # get new notification count
            notificationCount = 0
            for i in notViewednotifications:
                notificationCount += 1


        except BankingPerson.DoesNotExist:
            bankingP = None
    else:
        bankingP = None
    data = {
        "token" : c,
    }

    if bankingP != None: # if logged in, fetch the associated information
        data.update({
            "bankingPerson" : bankingP,
            "accounts": accounts,
            "notifications" : notifications,
            'notificationCount' : notificationCount,
            "totalAmount" : totalAmount,
            "user" : user,
            "userPk" : user.pk,
        })

    return data