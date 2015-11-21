# Code written by Plamen Kolev

from django import forms
from payment.models import BankingPerson, Account, OutgoingTransaction, SavedPayee
from django.utils import timezone
from django.core.exceptions import ValidationError


class OutgoingTransactionForm(forms.ModelForm):

    account = forms.ChoiceField()

    def __init__(self,*args, **kwargs):
        accounts = kwargs.pop('accounts') # the arguments are popped from the view wich looks like this TransactionForm(accounts = accountobject), used to fetch all accounts belonging to a person

        super(OutgoingTransactionForm, self).__init__(*args,**kwargs)

        choices = [] #
        # IF ZERO FIX ERROR !
        for acc in accounts: # generate a tuple of acc options
            choices.append((acc.accountNumber, acc.accountName + ' $' + str(acc.amount)))
        self.fields['account'].choices = choices

    class Meta:
        model = OutgoingTransaction # meta establishes a link between the model of a transaction and this form called Transaction form
        exclude = ('fromObject', 'fromAccount', 'balance', 'theDate') # doesn't render those fields inside the form html
        widgets = {
            'amount' : forms.TextInput(attrs={'placeholder': ''})
    }

class AccountRenameForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('accountName',)

class SavedPayeeForm(forms.ModelForm):
    class Meta:
        model = SavedPayee
        exclude = ("owner",)