# Code written by Plamen Kolev

from django import forms
from budget.models import MonthlyBudget, Purchase, Category, WishlistItem
from budget.widgets import MonthYearWidget
from budget.models import Category
class MonthlyBudgetForm(forms.ModelForm):

# snipped from https://djangosnippets.org/snippets/1688/
    date = forms.DateField(widget=MonthYearWidget(years=xrange(2015,2017)))

    class Meta:
        model = MonthlyBudget
        exclude = ("user",)

class PurchaseForm(forms.ModelForm):

    # def __init__(self, choices,*args, **kwargs):
    #     super(PurchaseForm, self).__init__(*args,**kwargs)

        # self.fields["category"].queryset = choices

    class Meta:
        model = Purchase
        exclude = ('budget',)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("spent",)

class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        exclude =("date","bought","user",)