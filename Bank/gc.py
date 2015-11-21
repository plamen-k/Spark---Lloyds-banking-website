from autofixture import AutoFixture
from content_controller.models import *
from django.contrib.auth.models import User
from payment.models import *
print "Creating superuser"
user = User.objects.create_user('root', 'll@gmail.com', 'toor')
user.is_superuser = True
user.is_staff = True
user.save()
for i in range(0,5):
	user = User.objects.create_user("user"+str(i), 'user'+str(i)+"@gmail.com", 'toor')
	fixture = AutoFixture(BankingPerson)
	user.save()
	fixture = AutoFixture(Account)
	account = fixture.create(2)
	account[0].owner = user
	account[1].owner = user
	account[1].amount = 200
	account[0].save
	account[1].save
	fixture = AutoFixture(OutgoingTransaction)
	entries = fixture.create(2)
	fixture = AutoFixture(IncomingTransaction)
	entries = fixture.create(2)
	fixture = AutoFixture(Slide)
	entries = fixture.create(2)
	fixture = AutoFixture(UserStory)
	entries = fixture.create(2)
	fixture = AutoFixture(Service)
	entries = fixture.create(3)
