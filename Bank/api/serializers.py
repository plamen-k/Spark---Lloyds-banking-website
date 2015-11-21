# Code written by Plamen Kolev

from django.core.exceptions import ValidationError
from rest_framework import serializers
from payment.models import OutgoingTransaction, BankingPerson, Account,SavedPayee, IncomingTransaction, SavedPayee
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from notification.models import Notification
from rest_framework.authtoken.models import Token

class OutgoingTransactionSerializer(serializers.ModelSerializer):

	owner = serializers.ReadOnlyField(source='owner.username')
	#
	def create(self, validated_data): # everytime this object is created, do a transaction
		fromAccountPk = int(validated_data['fromAccount'].pk)
		fromAccount = Account.objects.get(pk=fromAccountPk)
		result = fromAccount.transfer(
					api=True,
					name= validated_data['toName'],
					iban= validated_data['toIban'],
					sort= validated_data['toSortCode'],
					amount= validated_data['amount'],
					description= validated_data['description'],
		)

		if result == 1: # function returns a flag that cna be checked for succ/fail
			raise ValidationError("Details provided were incorrect!")
		outgoing = OutgoingTransaction(**validated_data)
		outgoing.owner = self.context['view'].request.user
		outgoing.fromUser = self.context['view'].request.user
		outgoing.save()
		return outgoing

	def get_fields(self, *args, **kwargs):
		fields = super(OutgoingTransactionSerializer, self).get_fields(*args, **kwargs)
		accounts = Account.objects.filter(owner = self.context['view'].request.user) # validate so that you dont fetch someone else's account
		# fields['fromUser'].queryset = User.objects.get(pk=self.context['view'].request.user.pk)
		fields['fromAccount'].queryset = accounts
		return fields

	class Meta:
		model = OutgoingTransaction
		fields = ('id', 'fromAccount', 'toName','theDate',
			'toSortCode', 'toIban','toName', 'amount','description', 'owner')

class IncomingTransactionSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = IncomingTransaction

class SavedPayeeSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = SavedPayee

class TokenSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Token

class AccountSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Account
		fields = ('id', 'accountName', 'accountNumber', 'sortCode', 'iban', 'amount', 'overdraft', 'owner')

class NotificationSerializer(serializers.ModelSerializer):
	# owner = serializers.ReadOnlyField(source='owner.username')
	class Meta:
		model = Notification
		fields = ('id','level', 'text', 'theDate')
class BankingPersonSerializer(serializers.ModelSerializer):

	class Meta:
		model = BankingPerson
		fields = ('user','phone', 'address','phone','receiveEmail','receiveDanger','receiveInfo','receiveSuccess','receiveWarning')

class SavedPayeeSerializer(serializers.ModelSerializer):
	api_owner = serializers.ReadOnlyField(source='owner.username')
	def create(self, validated_data):
		newpayee = SavedPayee(**validated_data)
		newpayee.owner = self.context['view'].request.user
		newpayee.save()
		return newpayee

	class Meta:
		model = SavedPayee
		fields = ('name', 'iban', 'sortCode', 'api_owner')