from django.test import TestCase
import django
from notification.models import Notification, MassNotification
from django.contrib.auth.models import User
from payment.models import Account, OutgoingTransaction
from payment.models import BankingPerson

# Create your tests here.
class notificationTestCase(django.test.TestCase):
    def setUp(self):
        randomName = "Matthew Perrie"
        newUser = User(username = randomName)
        newUser.first_name = randomName
        newUser.set_password(randomName)
        newUser.save()
        Notification.objects.create(title='Incoming transaction!', level=1, to=newUser, text='Test notification')

    def test_notification_can_be_created_correctly(self):
        user = User.objects.get(pk=1)
        notification = Notification.objects.get(pk=1)
        self.assertEquals(notification.to, user)
        self.assertEquals(notification.text, 'Test notification')
        self.assertEquals(notification.level, 1)
        self.assertEquals(notification.title, 'Incoming transaction!')
        self.assertEquals(notification.read, False)
        self.assertEquals(notification.viewed, False)

    def test_notification_can_be_read(self):
        notification = Notification.objects.get(pk=1)
        notification.markRead()
        self.assertEquals(notification.viewed, True)

    def test_transaction_creates_notification(self):
        user = User.objects.get(pk=1)
        newBankingPerson = BankingPerson.objects.get(user=user)
        newBankingPerson.owner = user
        newBankingPerson.save()

        acc1 = Account().create()
        acc1.accountName = "Savings Account"
        acc1.create()
        acc1.owner = user
        acc1.amount = 300
        acc1.save()

        acc2 = Account().create()
        acc2.accountName = "Savings Account"
        acc2.create()
        acc2.owner = user
        acc2.amount = 300
        acc2.save()

        acc1.transfer(name=acc2.accountName, iban=acc2.iban, sort=acc2.sortCode, amount=20, description="test")
        notification = Notification.objects.get(pk=2)

        self.assertEquals(notification.to, user)
        self.assertEquals(notification.level, 1)
        self.assertEquals(notification.title, 'Incoming transaction!')
        self.assertEquals(notification.read, False)
        self.assertEquals(notification.viewed, False)

