# Code written by Plamen Kolev

from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from payment.models import OutgoingTransaction, IncomingTransaction, BankingPerson
from Bank.views import baseDict
from userprofile.forms import UserSettingsForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

@login_required
def viewProfile(request):
    
    dictData = baseDict(request)
    bankingP = dictData['bankingPerson']
    outgoingTransactions = OutgoingTransaction.objects.filter(fromUser = request.user)
    incomingTransactions = IncomingTransaction.objects.filter(toUser = request.user)

    dictData.update({
        "outgoing": outgoingTransactions,
        "incoming": incomingTransactions,
    })

    return render_to_response("userprofile/profile.html", dictData,)

def changeSettings(request):
    dictData = baseDict(request)
    userData = get_object_or_404(BankingPerson, user=request.user)

    if request.method == 'POST':
        postData = request.POST
        form = UserSettingsForm(postData, instance=userData)

        if form.is_valid():
            form.save()
    else:
        form = UserSettingsForm(instance=userData)

    dictData.update({
        'form' : form,
    })

    return render_to_response("userprofile/forms/settingsForm.html", dictData,  context_instance=RequestContext(request))
    
@login_required
def lock(request):
    user = User.objects.get(username=request.user.username)
    if user is None:
        raise Exception
    else:
        user.active=False
        user.save()
    return HttpResponseRedirect("/logout")

def branch_finder(request):
    dictionary = baseDict(request)
    return render_to_response("map_finder.html", dictionary)


def student_account(request):
    dictionary = baseDict(request)
    return render_to_response("controller/student_account.html", dictionary)

def graduate_account(request):
    dictionary = baseDict(request)
    return render_to_response("controller/graduate_account.html", dictionary)

def budgeting_info(request):
    dictionary = baseDict(request)
    return render_to_response("controller/budgeting_info.html", dictionary)

def legal(request):
    dictionary = baseDict(request)
    return render_to_response("controller/legal.html", dictionary)