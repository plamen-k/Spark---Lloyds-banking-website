# Code written by Plamen Kolev

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
from colorful.fields import RGBColorField
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class MonthlyBudget(models.Model):
    status = models.CharField(max_length=155, blank=True)
    date = models.DateTimeField(auto_now_add=False, default=timezone.now())
    limit = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    user = models.ForeignKey(User)

    def __str__(self):
        return self.status + " " + str(self.date)

class WishlistItem(models.Model):
    title = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateTimeField(auto_now_add=False, default=timezone.now())
    user = models.ForeignKey(User)
    bought = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " " + str(self.date)

class Category(models.Model):
    title = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    budget = models.ForeignKey(MonthlyBudget)
    date = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
    color = RGBColorField()
    spent = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0)

    def __str__(self):
        return self.title + " " + unicode(self.budget.date)

class Purchase(models.Model):
    description = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    budget = models.ForeignKey(MonthlyBudget)
    theDate = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.description

@receiver(post_save, sender=MonthlyBudget)
def createDefaultCategoryForMonthlyBudget(sender, instance, **kwargs):
    category = Category()
    category.color = "#ececec"
    category.title= "Other"
    category.price = instance.limit
    category.budget = instance
    category.save()

# validates duplicate budgets
@receiver(pre_save, sender=MonthlyBudget)
def prevent_duplicate_monthly_budgets(sender, instance, **kwargs):
    try:
        collision = MonthlyBudget.objects.get(date__year=instance.date.year, date__month=instance.date.month, user=instance.user) # fetching the date must be filtered by month not by [01.20.30/12:00:00], as it will be invalid
        if collision != []:
            raise ValidationError("Budget for this month has been created")
    except MultipleObjectsReturned:

        raise ValidationError("Budget for this month has been created")
    except ObjectDoesNotExist:
        pass

@receiver(post_save, sender=Purchase)
def update_category_on_new_purchase(sender, instance, **kwargs):
    if kwargs['created']:
        cat = instance.category
        cat.spent+=instance.price
        cat.save()

# @receiver(pre_save, sender=Purchase)
# def remove_price_from_category_on_product_delete(sender, instance, **kwargs):
#     if not kwargs['created']:
#         cat = instance.category
#         cat.spent+=instance.price
