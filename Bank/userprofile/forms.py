# Code written by Plamen Kolev

from django import forms
from payment.models import BankingPerson
from django.contrib.auth.models import User


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = BankingPerson
        exclude = ('user','wishlistSpending')

class UserPasswordChangeForm(forms.ModelForm):
    class Meta:
        model = User