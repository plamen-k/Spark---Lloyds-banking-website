

# the code is part of django documentation on sindication
# https://docs.djangoproject.com/en/1.7/ref/contrib/syndication/

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from notification.models import MassNotification

class LatestEntriesFeed(Feed):

	title = "update me"
	link = "/notifications/feed/"
	description = "update me."

	def items(self):
		return MassNotification.objects.order_by('-theDate')[:5]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.text
