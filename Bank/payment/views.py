# Code written by Plamen Kolev

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from payment.models import BankingPerson, Account, OutgoingTransaction, IncomingTransaction,SavedPayee
from payment.forms import OutgoingTransactionForm, AccountRenameForm, SavedPayeeForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from Bank.views import baseDict
from datetime import timedelta, datetime
from rest_framework.authtoken.models import Token

@login_required
def sendMoney(request):

    dictData = baseDict(request)
    formError = [] # this string will send the template message about insufficient funds

    bankingPerson = dictData['bankingPerson']
    myAccounts = dictData['accounts']
    myPayeeList = SavedPayee.objects.filter(owner=request.user)
    if request.method == 'POST':
        # if the form has been submitted, validate it (if invalid,
        # all the valid fields before submission will remain)

        form = OutgoingTransactionForm(request.POST, accounts=myAccounts)
        # accounts and auto-fill are keys to arguments, they will be poped by the Transaction form in it's constructor
        if form.is_valid():
            transaction = form.save(commit = False)
        # to be removed transaction = form.save(commit=False)
        #  gets the data from the form as a transaction object (Transaction model in account.models)
            myAccount = Account.objects.get(owner__pk = bankingPerson.pk , accountNumber = form.cleaned_data['account'], owner = bankingPerson) # get the account that was submited in the drop down menu. Get will fail if not found and will throw error if more than one
            # same is done below, but it's more straight forward

            if (myAccount.amount + myAccount.overdraft) <= 0:  # Redundant check for spending more money than you have + your overdraft
                formError.append("Not enough cash to finish the transaction !")
            else: # if the account we want to send money to is fetched successful, we execute the model transfer function
                result = myAccount.transfer(name=transaction.toName,iban = transaction.toIban, sort = transaction.toSortCode, amount = transaction.amount, description = transaction.description)
                if result != 0:
                    formError.append("Check the details and try again !")
                else:

                    return redirect("index") # Maybe redirect somewhere else <- this is where everything went right
        else:
            formError.append("Please check name, sortcode or account number and try again. ")
    else: # that means there is no post data, so the form is generated from scratch
        form = OutgoingTransactionForm(accounts=myAccounts)

    dictData.update({
        'formError' : formError,
        'form': form,
        'payeeList': myPayeeList,
        'token': Token.objects.get(user=request.user),
    })

    return render_to_response('payment/forms/sendMoney_form.html', dictData, context_instance=RequestContext(request))
    # return HttpResponse("crap")

def save_to_payee(request):
    dictionary = baseDict(request)

    if request.method == "POST":
        form = SavedPayeeForm(request.POST)
        if form.is_valid():
            payee = form.save(commit=False)
            payee.owner = request.user
            payee.save()
            dictionary.update({
                "message": "Added to payee list!",
            })
            return render_to_response("alert.html", dictionary)
    else:
        form = SavedPayeeForm()
    dictionary.update({
        "form" : form,
    })
    return render_to_response("payment/forms/saved_payee_form.html", dictionary, context_instance=RequestContext(request))

@login_required
def statement(request, pk):
    dictData = baseDict(request)
    today = datetime.today().date()
    timeAgo = today - timedelta(days=30) # get transactions in the last 30 days
    outgoingTransaction = OutgoingTransaction.objects.filter(fromUser=request.user, fromAccount__pk=pk, theDate__gte = timeAgo)
    incomingTransaction = IncomingTransaction.objects.filter(toUser=request.user, toAccount__pk=pk, theDate__gte = timeAgo)

    dictData.update({
        'account' : Account.objects.get(owner=request.user, pk=pk),
        'outgoing' : outgoingTransaction,
        'incoming' : incomingTransaction,
    })

    return render_to_response("userprofile/statement.html", dictData)

@login_required
def change_account_name(request, pk):
    account = Account.objects.get(pk=pk)
    formError = [] # an array of potential errors
    dictionary = baseDict(request)
    if request.method == "POST":
        form = AccountRenameForm(request.POST)
        if form.is_valid():
            dictionary.update({
                "message" : "Account successfully renamed !",
            })
            account.accountName = form.cleaned_data['accountName']
            account.save()
            return render_to_response("alert.html",dictionary)
        else:
            formError.append("Please enter a valid input !")
    else:
        form = AccountRenameForm(instance = account)

    dictionary.update({
        "form" : form,
        "accountId" : pk,
    })

    return render_to_response("userprofile/forms/change_account_name.html", dictionary, context_instance=RequestContext(request))
