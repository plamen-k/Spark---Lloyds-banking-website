from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from payment.models import BankingPerson
from payment.models import Account
from django.contrib.auth.models import User
from notification.models import Notification
import random
import string
import random

def createSuperUser(request):

	nameList = ["Beth","Fox","Webster","Dallas","Kathleen","Steele"]

	# from http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
	try:
		theSuperman = User.objects.get(username='root')
	except User.DoesNotExist: 
		my_admin = User.objects.create_superuser('root', 'myemail@test.com', 'toor')
		my_admin.save()
		bankingRoot = BankingPerson(name = "BankingRoot", user=my_admin)
		bankingRoot.name = "Mr. Plamen Tatianski Kolev"
		bankingRoot.address = "Fenham Hall Drive, St. Marry College, NE6 5K1"
		bankingRoot.phone = "0886658547"
		bankingRoot.email = "nicemail@gmail.com"
		bankingRoot.save()
		acc1 = Account().create()
		acc1.accountName = "Student Account"
		acc2 = Account().create()
		acc2.accountName = "Savings Account"
		acc1.owner = bankingRoot
		acc2.owner = bankingRoot
		acc1.save()
		acc2.save()

	accNames = ["Savings account", "Mortgage", "Daily Account"]

	for i in xrange(1,len(nameList)-1):
		randomName = nameList[i]
		newUser = User(username = randomName)
		newUser.set_password(randomName)
		newUser.save()

		newAccount = BankingPerson(name=randomName)
		newAccount.user = newUser
		newAccount.save()
		for i in range(0, len(accNames)-1):
			newAcc = Account()
			newAcc.accountName = accNames[i]
			newAcc.create()
			newAcc.owner = newAccount
			newAcc.save()

	return redirect('index')

@login_required
def generateOutgoing(request):
	# key = random.uniform(1, 6) # used for random account transaction generation
	foreignAccount = Account.objects.get(pk = 3)
	foreignPerson = foreignAccount.owner
	# bankingPerson = BankingPerson.objects.get(user = request.user)
	myTransactionAccount = Account.objects.filter(owner=request.user)[0] #request.user.getAccounts()[0]
	myTransactionAccount.transfer( name=foreignPerson.username,iban=foreignAccount.iban, sort=foreignAccount.sortCode, amount=50, description="Test money")
	return redirect("/")

@login_required
def generateIncoming(request):
	myTransactionAccount = BankingPerson.objects.get(user = request.user).getAccounts()[0]
	
	accounts = Account.objects.all()
	key = int(random.uniform(1, len(accounts)))

	foreignAccount = Account.objects.get(pk=accounts[key].pk)
	foreignPerson = foreignAccount.owner
	foreignAccount.transfer(name=foreignPerson.username, iban = myTransactionAccount.iban, sort = myTransactionAccount.sortCode, amount = 50, description = "I sent plamen cash")
	return redirect("viewProfile")

def generateInfoNotification(request):
	user = request.user
	bankingP = BankingPerson.objects.get(user=user)
	if bankingP.receiveInfo:
		n = Notification(title="Information triggered", text="I thought him the queerest old Quaker I ever saw, especially as Peleg,his friend and old shipmate, seemed such a blusterer. But I said nothing, only looking round me sharply. Peleg now threw open a chest, and drawing forth the ship's articles, placed pen and ink before him, and seated himself at a little table. I began to think it was high time to settle with myself at what terms I would be willing to engage for the voyage. I was already aware that in the whaling business they paid no wages; but all hands, including the captain, received certain shares of the profits called lays, and that these lays were proportioned to the degree of importance pertaining to the respective duties of the ship's company. I was also aware that being a green hand at whaling, my own lay would not be very large; but considering that I was used to the sea, could steer a ship, splice a rope, and all that, I made no doubt that from all I had heard I should be offered at least the 275th lay--that is, the 275th part of the clear net proceeds of the voyage, whatever that might eventually amount to. And though the 275th lay was what they call a rather LONG LAY, yet it was better than nothing; and if we had a lucky voyage, might pretty nearly pay for the clothing I would wear out on it, not to speak of my three years' beef and board, for which I would not have to pay one stiver.", level = 0, to=user)
		n.save()
	return HttpResponseRedirect("/")
	
def generateSuccessNotification(request):
	user = request.user
	bankingP = BankingPerson.objects.get(user=user)
	print bankingP.receiveSuccess
	if bankingP.receiveSuccess:
		n = Notification(title="Success may be on your way", text="hello world body", level = 1, to=user)
		n.save()
	return HttpResponseRedirect("/")

def generateWarningNotification(request):
	user = request.user
	bankingP = BankingPerson.objects.get(user=user)
	if bankingP.receiveWarning:
		n = Notification(title="BE WARNED, mortal", text="But one thing, nevertheless, that made me a little distrustful about receiving a generous share of the profits was this: Ashore, I had heard something of both Captain Peleg and his unaccountable old crony Bildad; how that they being the principal proprietors of the Pequod, therefore the other and more inconsiderable and scattered owners, left nearly the whole management of the ship's affairs to these two. And I did not know but what the stingy old Bildad might have a mighty deal to say about shipping hands, especially as I now found him on board the Pequod, quite at home there in the cabin, and reading his Bible as if at his own fireside. Now while Peleg was vainly trying to mend a pen with his jack-knife, old Bildad, to my no small surprise, considering that he was such an interested party in these proceedings; Bildad never heeded us, but went on mumbling to himself out of his book, 'LAY not up for yourselves treasures upon earth, where moth.", level = 2, to=user)
		n.save()
	return HttpResponseRedirect("/")

def generateDangerNotification(request):
	user = request.user
	bankingP = BankingPerson.objects.get(user=user)
	if bankingP.receiveDanger:
		n = Notification(title="Danger danger, we're gonna die", text="LAY, indeed, thought I, and such a lay! the seven hundred and seventy-seventh! Well, old Bildad, you are determined that I, for one, shall not LAY up many LAYS here below, where moth and rust do corrupt. It was an exceedingly LONG LAY that, indeed; and though from the magnitude of the figure it might at first deceive a landsman, yet the slightest consideration will show that though seven hundred and seventy-seven is a pretty large number, yet, when you come to make a TEENTH of it, you will then see, I say, that the seven hundred and seventy-seventh part of a farthing is a good deal less than seven hundred and seventy-seven gold doubloons; and so I thought at the time.", level = 3, to=user)
		n.save()
	return HttpResponseRedirect("/")
