# Code written by Plamen Kolev

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from notification.models import Notification
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.contrib.auth.signals import user_logged_in
import random
import string
from rest_framework.authtoken.models import Token

# TODO make a sql table when a collision happens
# Validators (does the account number length and the sort code)
def validate_iban(value):
    validationDigit = 22 # set the value for custom account digits
    digitLength = len(str(value))#length of digits
    if digitLength != validationDigit:
        raise ValidationError("Iban number must be %d digit, %d given instead !" % (validationDigit, digitLength))

def validate_sort(value):
    validationDigit = 6 # set the value for custom account digits
    digitLength = len(str(value))
    if digitLength != validationDigit:
        raise ValidationError("Sort-code must be %d digit, %d given instead !" % (validationDigit, digitLength))

def validate_transaction_amount(value):
    if value <= 0:
        raise ValidationError("The field cannot be zero or negative !")
# End of validators

class SavedPayee(models.Model):
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=22, validators = [validate_iban])
    sortCode = models.CharField(max_length=6, validators = [validate_sort])
    owner = models.ForeignKey(User)

class UserLogin(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())

class BankingPerson(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    address = models.CharField(max_length=600)
    phone = models.CharField(max_length=12)
    email= models.CharField(max_length=300)
    receiveEmail = models.BooleanField(default=True)
    receiveInfo = models.BooleanField(default=True)
    receiveSuccess = models.BooleanField(default=True)
    receiveWarning = models.BooleanField(default=True)
    receiveDanger = models.BooleanField(default=True)
    dateCreated = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
    safeDialCode = models.CharField(max_length=4)
    wishlistSpending = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    def getAccounts(self): # method for fetching all the accounts associated with a person
        return Account.objects.filter(owner__pk = self.pk) # filter works, because account has an owner, so the query looks for the primary key of the owner, wich is the owner object's pk

    def __str__(self):		 # tostring method
        return str(self.user.username)

# Validate transfer also simulates a foreign bank
class OutgoingTransaction(models.Model): # This class represents a bank transfer between two parties and is used by the accounts.forms under TransactionForm

    fromUser = models.ForeignKey(User)
    fromAccount = models.ForeignKey('Account')
    toName = models.CharField(max_length=200)
    toSortCode = models.CharField(max_length = 6, validators = [validate_sort])
    toIban = models.CharField(max_length=22, validators = [validate_iban])
    amount = models.FloatField(validators=[validate_transaction_amount])
    balance = models.FloatField(blank=True) # how much money was the balance at this time
    theDate = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return str(self.amount) + " from " + str(self.fromUser) + " to " + str(self.toName)

class IncomingTransaction(models.Model):
    toUser = models.ForeignKey(User)
    toAccount = models.ForeignKey('Account')
    fromName = models.CharField(max_length=200)
    fromIban = models.CharField(max_length=22)
    amount = models.FloatField(validators=[validate_transaction_amount])
    balance = models.FloatField() # how much money was the balance at this time
    theDate = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=30)

    def __str__(self):
        return 'Received %s from %s' % (self.amount, self.fromName)

class Account(models.Model):

    accountName = models.CharField(max_length = 200)
    accountNumber = models.CharField(max_length=8)
    sortCode = models.IntegerField( validators=[validate_sort], max_length = 6) #[00-00-00]
    iban = models.CharField(max_length = 22, validators=[validate_iban]) #[BG16 RZBB 9155 8520 0224 29]
    amount = models.FloatField()
    overdraft = models.FloatField()
    owner = models.ForeignKey(User)

    def __str__(self): # also known as toString method in java, everywhere where you print an account object will call this method ( admin, shell html/template ).

        accPrint = str(self.iban) # Get the value to print and convert it to string for more flexible manipulation
        newstring = "" 										 # create the empty string that will contain the xxxx-xxxx-xxxx-xxxx separation
        for i in range(0,len(accPrint)): # Iterate over each character in the long digit
            newstring += accPrint[i]
            if (i+1) % 4 == 0: 							 # iterate through the account number string and add a "-" every 4th place, counter<15 is so that the re is no dash at the end
                newstring += '-'
        return str(newstring)

# transfers money from "this" account to a foreign accound
    def transfer(self, **kwargs): # parameters are the name, sort code, account number of the destination and the amount
        api = False # by default a transfer is not an api call
        name=kwargs.get('name')
        iban=kwargs.get('iban')
        sort=kwargs.get('sort')
        amount=kwargs.get('amount')

        api = kwargs.get('api')

        if api is not None:
            api = bool(api)

# debug
        if api:
            print "Transaction is an api call"
# debug

        # validate kwargs here
        if name is None or iban is None or sort is None or amount is None:
            raise ValidationError("The arguments are name, iban, sort and amount. The function also takes optional description argument.")
        if 'description' in kwargs:
            description=kwargs.get('description')
        else:
            description = 'no description'

        # if remoteAccount was not fetched, that will throw an error, otherwise the below code will be executed
        if (self.amount-amount+self.overdraft) < 0:
            raise ValidationError("You don't have enough funds to do the transaction")	# for redundancy, this checks if you can remove money from you

        if validate_transfer(self, name, iban, sort, amount, description):
            bankingP = BankingPerson.objects.get(user = self.owner)

            if not api:
                oTransaction = OutgoingTransaction(fromUser = self.owner, fromAccount = self, toSortCode = sort, toName = name, toIban = iban, amount = amount, description = description, balance = self.amount)
                oTransaction.save()
            # generate a notification under certain circumstances
            if self.amount >= 0 and self.amount < 50:
                if bankingP.receiveWarning:
                    Notification.objects.create(title='Low Balance Alert!', level=2, to=self.owner, text='Warning, your balance is %s' % self.amount)
            elif self.amount<0:
                if bankingP.receiveDanger:
                    Notification.objects.create(title='You are in overdraft!', level=3, to=self.owner, text='Warning, your balance is in overdraft, current amount is %s' % self.amount)
            else:
                pass

            return 0
        else:
            return 1

    def create(self): # Automation script for creating a new account of a certain type
        # from http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
        # check if sort or account number is unique
        collision=True # assume collision has occurred, check with the database and then move on

        while(collision): # while there is a collision, generate an account and sort code
            iban = 0
            sortCode = 0
            while(len(str(iban)) != 22): # sometimes a number will be appended by zero, so this is required
                iban = int(random.random() * 10000000000000000000000)
            while(len(str(sortCode)) != 6):
                sortCode = int(random.random() * 1000000)

            try: # check if a collision has been encountered
                Account.objects.get(iban=iban)
                Account.objects.get(sortCode=sortCode)

            except Account.DoesNotExist: # if not, stop the while loop
                collision = False

        # endcheck
        self.iban = iban # set account number of the new account
        self.sortCode = sortCode 		# and the sortcode

        # now the account number is the reminder last 8 digits of the iban
        self.accountNumber = int(str(iban)[-8:])
        self.overdraft = 200 		# set the default overdraft
        self.amount = 200 			# set initial amount
        return self # function returns an account object

def validate_transfer(fromAccount, name, iban, sortCode, amount, description): # this function is used by transfer as the success/fail flag, it will tell it if an entry exists, thus transaction is successful. The function simulates another bank api call.
    if amount <= 0:
        return False
    try:
        bankAccount = Account.objects.get(iban=iban, sortCode=sortCode) # fetch the bank account
        theUser = bankAccount.owner
        bankingP = BankingPerson.objects.get(user=theUser)
    except Account.DoesNotExist:
        bankAccount = None

    if bankAccount is not None: # if account is found

        incoming = IncomingTransaction() # make a transaction object
        incoming.toUser = User.objects.get(account = bankAccount)
        incoming.toAccount = bankAccount
        incoming.fromName = name
        incoming.fromIban = iban
        incoming.description = description
        incoming.amount =  amount
        incoming.balance = bankAccount.amount
        incoming.save()

        if bankingP.receiveInfo: # notify
            Notification.objects.create(title='Incoming transaction!', level=1, to=theUser, text='%s sent you %s in %s, current balance is %s' % (name, amount, bankAccount.accountName, bankAccount.amount))

        if bankAccount.pk != fromAccount.pk:
            bankAccount.amount += amount
            bankAccount.save()

            fromAccount.amount -= amount
            fromAccount.save()

        return True
    else:
        return False

@receiver(pre_save, sender=OutgoingTransaction) # signal function that autoupdates the outgoing transaction with the current balance
def updateBalance(sender, instance, **kwargs):
    instance.balance = instance.fromAccount.amount - instance.amount

@receiver(post_save, sender=User) # autocreates banking person everytime a new user is made
def createBankingUser(sender, instance, **kwargs):
    p = BankingPerson.objects.get_or_create(user=instance)
    Token.objects.get_or_create(user=instance)


def user_log(sender, user, request, **kwargs):
    newlog = UserLogin()
    newlog.user=request.user
    newlog.save()
user_logged_in.connect(user_log)