# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns
from notification.feeds import LatestEntriesFeed

urlpatterns = patterns('',

	url(r'markRead/(?P<pk>\d+)', 'notification.views.markRead', name='markRead'),
	url(r'markAllRead', 'notification.views.markAllRead', name='markAllRead'),
	url(r'all', 'notification.views.all', name='all'),
	url(r'markAllViewed', 'api.views.markNotificationsViewed', name='markAllViewed'),
	url(r'fullMessage/(?P<pk>\d+)', 'notification.views.fullMessage', name='fullMessage'),

	url(r'feed', LatestEntriesFeed()),




)