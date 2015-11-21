# Code written by Plamen Kolev

from payment.models import OutgoingTransaction, Account, SavedPayee, IncomingTransaction, BankingPerson
from payment.models import BankingPerson as BP
from api.serializers import OutgoingTransactionSerializer, AccountSerializer, TokenSerializer, BankingPersonSerializer, NotificationSerializer, SavedPayeeSerializer, IncomingTransactionSerializer
from rest_framework import generics
from rest_framework import permissions
from django.core import serializers
from django.http import HttpResponse
from content_controller.models import UserStory
from django.contrib.auth.models import User
from notification.models import Notification
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json
#asd
#  api calls from jquery

def markNotificationsViewed(request):

    notViewedNotifications = Notification.objects.filter(to=request.user, viewed=False)
    for i in notViewedNotifications:
        i.viewed = True
        i.save()
    print "api call done"
    return HttpResponse("Done")

# endapi for jquery

class IsOwnerOrReadOnly(permissions.BasePermission): # permission classes from djangorest documentation

    def check_object_permission(self, user, obj):
        return (user and user.is_authenticated() and (user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
             return True

        # Write permissions are only allowed to the owner of the snippet.
        # return self.check_object_permission(request.user, obj)
        if request.method == 'POST':
            return True
        else:
            return False

class GetSafedialKey(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    def get_object(self, number, username):
        try:
            bp = get_object_or_404(BP, user__username=username)

            if bp.safeDialCode == number:
                return Token.objects.get(user=bp.user)
            else:
                raise Http404
        except Token.DoesNotExist:
            raise Http404

    def get(self, request, number, username, format=None):
        token = self.get_object(number, username)
        serializer = TokenSerializer(token)
        return Response(serializer.data)

def getUserStories(request):
    userStories = serializers.serialize("json", UserStory.objects.all())
    return HttpResponse(json.dumps(userStories), content_type='application/json')


class OutgoingTransactionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.filter(owner=self.request.user)
    serializer_class = OutgoingTransactionSerializer

    def get_queryset(self):
        return OutgoingTransaction.objects.filter(fromUser=self.request.user)

class IncomingTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.all()
    serializer_class = IncomingTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return OutgoingTransaction.objects.filter(toUser=self.request.user)

class IncomingTransactionList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.filter(owner=self.request.user)
    serializer_class = IncomingTransactionSerializer

    def get_queryset(self):
        return IncomingTransaction.objects.filter(toUser=self.request.user)

class OutgoingTransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.all()
    serializer_class = OutgoingTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return OutgoingTransaction.objects.filter(fromUser=self.request.user)

class BankingPerson(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = BankingPerson.objects.all()
    serializer_class = BankingPersonSerializer

    # def get_queryset(self):
    #   return BankingPerson.objects.get(owner=self.request.user)

class NotificationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.filter(owner=self.request.user)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(to=self.request.user)

class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(to=self.request.user)

class AccountList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    # queryset = OutgoingTransaction.objects.filter(owner=self.request.user)
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

class SavedPayeeList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    serializer_class = SavedPayeeSerializer

    def get_queryset(self):
        return SavedPayee.objects.filter(owner=self.request.user)

class SavedPayeeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    serializer_class = SavedPayeeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return SavedPayee.objects.filter(owner=self.request.user)


# from djangorestframework tutorial/documentation
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
