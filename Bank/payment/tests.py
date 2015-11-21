from django.test import TestCase
from django.test import Client
import django
from payment.models import Account, OutgoingTransaction, IncomingTransaction
from payment.models import BankingPerson
from django.contrib.auth.models import User

# Create your tests here.
class PaymentTestCase(django.test.TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('root2', 'myemail@test.com', 'toor2')
        my_admin.first_name = "Mr. Plamen Tatianski Kolev"
        my_admin.save()

        bankingRoot = BankingPerson.objects.get(user=my_admin, user__first_name = my_admin.first_name)
        bankingRoot.address = "Fenham Hall Drive, St. Marry College, NE6 5K1"
        bankingRoot.phone = "0886658547"
        bankingRoot.email = "nicemail@gmail.com"
        bankingRoot.save()

        acc1 = Account().create()
        acc1.accountName = "Student Account"
        acc1.amount = 200
        acc2 = Account().create()
        acc2.accountName = "Savings Account"
        acc2.amount = 200
        acc1.owner = my_admin
        acc2.owner = my_admin
        acc1.save()
        acc2.save()

        randomName = "Matthew Perrie"
        newUser = User(username = randomName)
        newUser.first_name = randomName
        newUser.set_password(randomName)
        newUser.save()

        newBankingPerson = BankingPerson.objects.get(user=newUser)
        newBankingPerson.owner = newUser
        newBankingPerson.save()

        acc3 = Account().create()
        acc3.accountName = "Savings Account"
        acc3.create()
        acc3.owner = newUser
        acc3.amount = 300
        acc3.save()

    def test_created_accounts_are_correct(self):
         acc1 = Account.objects.get(pk=1)
         acc2 = Account.objects.get(pk=2)
         acc3 = Account.objects.get(pk=3)
         # things we know about the first account
         self.assertEqual(acc1.owner.first_name,"Mr. Plamen Tatianski Kolev" )
         self.assertEqual(acc1.accountName, "Student Account")
         self.assertEqual(acc1.amount, 200)
         # things we know about the second account
         self.assertEqual(acc2.owner.first_name, "Mr. Plamen Tatianski Kolev")
         self.assertEqual(acc2.accountName, "Savings Account")
         self.assertEqual(acc2.amount, 200)
         # things we know about the third account
         self.assertEqual(acc3.owner.first_name, "Matthew Perrie")
         self.assertEqual(acc3.accountName, "Savings Account")
         self.assertEqual(acc3.amount, 300)

         # we know iban should be a unique number
         self.assertNotEqual(acc1.iban, acc2.iban)
         self.assertNotEqual(acc1.iban, acc3.iban)
         self.assertNotEqual(acc2.iban, acc3.iban)

    def test_one_transaction_can_be_made(self):
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=3)
        to_account_name = to_account.owner
        to_account_iban = to_account.iban
        to_account_sort = to_account.sortCode
        from_account.transfer(name=to_account_name, iban=to_account_iban, sort=to_account_sort, amount=20, description="test")
        to_account = Account.objects.get(pk=3)
        self.assertEqual(to_account.amount, 320)
        self.assertEqual(from_account.amount, 180)

    def test_many_transactions_can_be_made(self):
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        for i in range(0, 1000):
            from_account.transfer(name=to_account.owner, iban=to_account.iban, sort=to_account.sortCode, amount=0.001)
            from_account = Account.objects.get(pk=1)
            to_account = Account.objects.get(pk=2)
        #rounding errors happen so assertEquals will cause the test to fail - confirmed
        self.assertAlmostEqual(to_account.amount, 201)
        self.assertAlmostEqual(from_account.amount, 199)

    # this first test ensures that money will not be taken from an account if invalid data is entered
    def test_invalid_transactions_cannot_be_made(self):
        from_account = Account.objects.get(pk=1)
        from_account.transfer(name='test', iban=0, sort=0, amount = 10)
        self.assertEqual(from_account.amount, 200)

    #def test_transactions_with_invalid_name_cannot_be_made(self):
    #   from_account = Account.objects.get(pk=1)
      #  to_account = Account.objects.get(pk=2)
       # from_account.transfer(name='invalid name', iban=to_account.iban, sort=to_account.sortCode, amount=10)
        #from_account = Account.objects.get(pk=1)
        #to_account = Account.objects.get(pk=2)
        #self.assertEqual(from_account.amount, 200)
        #self.assertEqual(to_account.amount, 200)

    def test_transactions_with_invalid_iban_cannot_be_made(self):
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        from_account.transfer(name=to_account.owner, iban=0, sort=to_account.sortCode, amount=10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)

    def test_transactions_with_invalid_sort_code_cannot_be_made(self):
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        from_account.transfer(name=to_account.owner, iban=to_account.iban, sort=0, amount=10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)

    def test_transactions_with_invalid_amount_cannot_be_made(self):
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        from_account.transfer(name=to_account.owner, iban=to_account.iban, sort=to_account.sortCode, amount=-10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)

    def test_transactions_with_valid_but_not_existing_iban_cannot_be_made(self):
        #iban is a 22 digit unique number
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        #if the first digit is not 0 then have our test iban start with a 0
        if to_account.iban[0]!=0 :
            test_iban = '0'+to_account.iban[1:]
        else :
            test_iban = '1'+to_account.iban[1:]
        # now we have an iban which has a different first digit to the original iban of the to_account
        # meaning it is a valid iban but the chances of it existing are minimal (there are only 3 other
        # accounts created in this test
        from_account.transfer(name=to_account.owner, iban=test_iban, sort=to_account.sortCode, amount=10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)

    def test_transactions_with_valid_but_not_existing_sort_code_cannot_be_made(self):
        #sort code is a 6 digit non-unique number
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        check_account = Account.objects.get(pk=3)
        # so we have all 3 created accounts, now let us create a valid sort code to test and
        # make sure it is unique
        test_sort = from_account.sortCode+1
        while (test_sort==from_account.sortCode or test_sort==check_account.sortCode):
            test_sort = test_sort+1

        from_account.transfer(name=to_account.owner, iban=to_account.iban, sort=test_sort, amount=10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)

    # sort code is treated as in integer value rather than unicode like iban is
    # here we show it cannot start with a 0 - it gets truncated to a 1 which then does
    # not validate in the transfer and no transaction is made

    def test_if_sort_code_is_integer(self):
        #sort code is a 6 digit non-unique number
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        to_account.sortCode = 000001
        print(to_account.sortCode)
        from_account.transfer(name=to_account.owner, iban=to_account.iban, sort=1, amount=10)
        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        self.assertEqual(from_account.amount, 200)
        self.assertEqual(to_account.amount, 200)