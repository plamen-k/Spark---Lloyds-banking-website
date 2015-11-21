# Code written by Plamen Kolev

from django.contrib import admin
from budget.models import MonthlyBudget, Purchase, Category, WishlistItem
# Register your models here.

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['description', 'price','budget']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'budget', 'spent']

admin.site.register(MonthlyBudget,)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(WishlistItem,)

