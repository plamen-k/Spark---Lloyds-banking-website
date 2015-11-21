# Code written by Plamen Kolev

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from Bank.views import baseDict
from budget.models import MonthlyBudget, Purchase, Category, WishlistItem
from budget.forms import MonthlyBudgetForm, PurchaseForm, CategoryForm, WishlistItemForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import datetime# used to get current month's budget
from calendar import monthrange


# Create your views here.
@login_required
def main(request):
    dictionary = baseDict(request) # get core data
    today = datetime.date.today()
    try: # might throw a non setup budget error
        currentMonthlyBudget = MonthlyBudget.objects.get(date__year=today.year, date__month=today.month, user=request.user)
        # fetch the current budget
        monthlyPurchaseList = Purchase.objects.filter(budget=currentMonthlyBudget)
        # fetch all items bought during that period
        totalSpentMonth = 0
        for purchase in monthlyPurchaseList:
            totalSpentMonth += purchase.price

        # this is the logic for creating the bar graph
        categoryPercent = [] # used to construct the counter
        spentPercent = []
        categories = Category.objects.filter(budget = currentMonthlyBudget)
        if currentMonthlyBudget.limit == 0:
            raise Exception('Division by zero !')
        for category in categories:
            categoryPercent.append(100 * category.price/currentMonthlyBudget.limit) # percentify the vlaues
            spentPercent.append(100 * category.spent/category.price)
        # bargraph logic ends here

        # get cat picture segment
        # get spent so far
        spent = 0
        purchases = Purchase.objects.filter(budget=currentMonthlyBudget)
        for purchase in purchases:
            spent += purchase.price

        monthLen = monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1] # get the length of current month (28,30,31 days)
        avgSpent = int(spent/datetime.datetime.today().day) # normalize, get average spent so far
        avgTotal = currentMonthlyBudget.limit / monthLen # get total monthly average

        ratio = int(avgSpent*avgTotal/100) # generate meme based on these values

        meme = get_meme_picture(ratio)

        dictionary.update({
            "currentBudget": currentMonthlyBudget,
            "purchases": monthlyPurchaseList,
            "total": totalSpentMonth,
            "date" : datetime.datetime.now().strftime("%B, %Y"),
            "categories": zip(Category.objects.filter(budget__user = request.user), categoryPercent, spentPercent ),
            "meme": meme,
        })
    except ObjectDoesNotExist:
        pass
    return render_to_response("budget/main.html", dictionary)

@login_required
def get_saved_money(request):
    now = datetime.datetime.now()
    dictionary = baseDict(request)
    second_date = datetime.date(now.year, now.month-1,1)
    pastBudgets = MonthlyBudget.objects.filter(date__lte=second_date)
    totalSaved = 0

    savingsCategories = []
    for pbudget in pastBudgets:
        savingsCategories.append(Category.objects.filter(budget=pbudget))
    total = 0
    spent = 0

    for i in savingsCategories:
        total += i[0].price
        spent += i[0].spent + dictionary['bankingPerson'].wishlistSpending

    dictionary.update({
        'pastSavings':  pastBudgets,
        'saved': total-spent,
        'wishlist': WishlistItem.objects.filter(user=request.user, bought=False),
    })

    return render_to_response("budget/get_saved_money.html", dictionary)

@login_required
def mark_wishlist_purchased(request, pk):
    dictionary = baseDict(request)

    purchased = WishlistItem.objects.get(pk=pk)
    purchased.bought = True
    bp = dictionary['bankingPerson']
    bp.wishlistSpending += purchased.price
    bp.save()
    purchased.save()
    now = datetime.datetime.now()
    dictionary = baseDict(request)
    second_date = datetime.date(now.year, now.month-1,1)
    pastBudgets = MonthlyBudget.objects.filter(date__lte=second_date)
    totalSaved = 0

    savingsCategories = []
    for pbudget in pastBudgets:
        savingsCategories.append(Category.objects.filter(budget=pbudget))
    total = 0
    spent = 0

    for i in savingsCategories:
        total += i[0].price
        spent += i[0].spent + dictionary['bankingPerson'].wishlistSpending

    dictionary.update({
        'pastSavings':  pastBudgets,
        'saved': total-spent,
        'wishlist': WishlistItem.objects.filter(user=request.user, bought=False),
    })

    return render_to_response("budget/get_saved_money.html", dictionary)

@login_required
def monthly_budget_setup(request): # this handles the form that will create the new budget
    dictionary = baseDict(request)
    formError = []
    if request.method == "POST": # submitted post validation
        form = MonthlyBudgetForm(request.POST)
        if form.is_valid():
            monthlyBudget = form.save(commit=False)
            monthlyBudget.user = request.user

            monthlyBudget.save()
            dictionary.update({
                "message" : "Budget successfully added !",
            })
            return render_to_response("alert.html",dictionary)

    else:
        form = MonthlyBudgetForm()

    dictionary.update({
        "form" : form,
        "formError" : formError,
    })
    return render_to_response("budget/forms/monthly_budget_form.html", dictionary, context_instance=RequestContext(request))

@login_required
def budget_add_purchase(request): # add a new purhcase to budget
    today = datetime.date.today()
    dictionary = baseDict(request)
    budget = MonthlyBudget.objects.get(date__year=today.year, date__month=today.month, user=request.user) # get budget based on current date
    category_choices = Category.objects.filter(budget=budget) # get all categories you have added as options

    if request.method == 'POST':
        
        form = PurchaseForm(request.POST) # recreate a form with autofiled dropdown categories according to budget
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.budget = budget
            purchase.save()
            dictionary.update({
                "message" : "Product added !",
            })
            return render_to_response("alert.html",dictionary)
    else:
        form = PurchaseForm()
    dictionary.update({
        "form": form,
    })
    return render_to_response("budget/forms/new_purchase_form.html", dictionary, context_instance=RequestContext(request))

def add_category(request):
    dictionary = baseDict(request)
    today = datetime.date.today()
    formError = []

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            monthlyBudget = form.cleaned_data['budget'].pk
            newCategoryPrice = form.cleaned_data['price']
            otherCategory = Category.objects.get(budget=monthlyBudget, title="Other", date__year=today.year, date__month=today.month,) # fetch the other section so you can decrease the amount, also for validation
            if otherCategory.price - otherCategory.spent < newCategoryPrice:
                formError.append("You can allocate " + str(otherCategory.price - otherCategory.spent) + ", but you tried to add " + str(newCategoryPrice))
            else:
                otherCategory.price -= newCategoryPrice # if the amount is not exeeding the other category, decrease the other category and create a new one
                otherCategory.save()
                form.save()
                dictionary.update({
                    "message" : "Category added !",
                })
                return render_to_response("alert.html",dictionary)

    else:
        form = CategoryForm()

    dictionary.update({
        "form": form,
        "formError": formError,
    })

    return render_to_response("budget/forms/add_category.html", dictionary, context_instance=RequestContext(request))

@login_required
def past_budgets(request): # fetch past budgets
    dictionary = baseDict(request)
    budgets = MonthlyBudget.objects.all()
    dictionary.update({
        "budgets" : budgets, 
    })
    return render_to_response("budget/past_budgets.html", dictionary)

@login_required
def single_budget_view(request,pk): # that budget overview
    dictionary = baseDict(request)
    budget = MonthlyBudget.objects.get(pk=pk)
    purchases = Purchase.objects.filter(budget=budget)
    spent = 0
    for purchase in purchases:
        spent+=purchase.price
        
    dictionary.update({
        "budget":budget,
        "purchases" : purchases,
        "spent" : spent,
    })
    return render_to_response("budget/single_budget_view.html", dictionary)

@login_required
def wishlist(request, pk):
    dictionary = baseDict(request)
    wishlistItems = WishlistItem.objects.all()

    dictionary.update({
        "wishlistItems" : wishlistItems,
    })
    return render_to_response("budget/wishlist.html", dictionary)
    
@login_required
def create_wishlist_item(request):

    dictionary = baseDict(request)
    if request.method == 'POST':
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = request.user
            wishlist_item.save()
            wishlistItems = WishlistItem.objects.all()

            dictionary.update({
                "wishlistItems" : wishlistItems,
            })
            return render_to_response("budget/get_saved_money.html", dictionary)
        else:
            return HttpResponse("gello")
    else:
        form = WishlistItemForm()
    dictionary.update({
        "form" : form,
    })

    return render_to_response("budget/forms/create_wishlist_item.html", dictionary, context_instance=RequestContext(request))

def get_meme_picture(karma):
    if karma >= 8:
        return "images/kittens/" + str(1) + ".jpg"

    if karma <= 0:
        return "images/kittens/" + str(8) + ".jpg"

    else:
        return "images/kittens/" + str(9-karma) + ".jpg"
