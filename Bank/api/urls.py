# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns
from django.contrib import admin
import Bank,api,views
from rest_framework.authtoken import views as tokenview

urlpatterns = patterns('',

    url(r'^accounts/$', api.views.AccountList.as_view()),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.AccountDetail.as_view()),
    
    url(r'^userstories$', 'api.views.getUserStories', name='userStories'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.BankingPerson.as_view()),

    url(r'^safedial/token/(?P<number>[0-9]+)/(?P<username>\w+)$', views.GetSafedialKey.as_view()),


    url(r'^notifications/$', views.NotificationList.as_view()),
    url(r'^notifications/(?P<pk>[0-9]+)/$', views.NotificationDetail.as_view()),
    url(r'^markViewed/$', 'api.views.markNotificationsViewed', name='markNotificationsViewed'),
    
    url(r'^outgoing/$', views.OutgoingTransactionList.as_view()),
    url(r'^outgoing/(?P<pk>[0-9]+)/$', views.OutgoingTransactionDetail.as_view()),

    url(r'^incoming/$', views.IncomingTransactionList.as_view()),
    url(r'^incoming/(?P<pk>[0-9]+)/$', views.IncomingTransactionDetail.as_view()),

    url(r'^savedpay/$', views.SavedPayeeList.as_view(), name="savedpay"),
    url(r'^savedpay/(?P<pk>[0-9]+)/$', views.SavedPayeeDetail.as_view()),

    # AUTH
    url(r'^auth/$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token/$', tokenview.obtain_auth_token),

# api urls
)
