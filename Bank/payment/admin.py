from django.contrib import admin
from payment.models import Account, OutgoingTransaction, IncomingTransaction, BankingPerson, SavedPayee, UserLogin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# passed as a parameter alongside Account, the list_display names are the visible fields in the admin section
class AccountAdmin(admin.ModelAdmin):
    list_display = ['accountName' ,'pk', 'owner', 'formattedSortCode', 'formatted_Account_Number', 'amount']

    def formatted_Account_Number(self, object): # a function that is passed in the list, also ilustrates how custom methods can be written. The field in the admin panel will also have this name
        return object

    def formattedSortCode(self, object):
        sortPrint = str(object.sortCode)
        newstring = ""
        for i in range(0,len(sortPrint)): # Iterate over each character in the long digit
            newstring += sortPrint[i]
            if (i+1) % 2 == 0: 							 # iterate through the account number string and add a "-" every 4th place, counter<15 is so that the re is no dash at the end
                newstring += '-'
        return str(newstring)

class ChildAccounts(admin.TabularInline): # renders in the banking person the associated bank accounts via inline, that inline is registered below
    model = Account

class TheUserAdmin(UserAdmin):
    list_display = ['pk', 'username', 'date_joined' ]
    inlines = [ ChildAccounts, ]

class OutgoingTransactionAdmin(admin.ModelAdmin):
    list_display = ['fromUser', 'pk', 'description', 'toName', 'toIban','amount', 'theDate']

class BankingPersonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(IncomingTransaction,)
admin.site.register(OutgoingTransaction, OutgoingTransactionAdmin)
admin.site.unregister(User)
admin.site.register(BankingPerson, BankingPersonAdmin)
admin.site.register(User, TheUserAdmin)
admin.site.register(SavedPayee, )
admin.site.register(UserLogin,)