# Code written by Plamen Kolev

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Notification(models.Model):
	OPTIONS = (
		(0, "info"),
		(1, "success"),
		(2, 'warning'),
		(3, 'danger'),
	)

	title 	= models.CharField(max_length=500)
	level 	= models.IntegerField(choices=OPTIONS, max_length=20)
	text 		= models.TextField()
	to 			= models.ForeignKey(User)
	viewed 	= models.BooleanField(default=False)
	read   	= models.BooleanField(default=False)
	theDate = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.title) + " - to " + str(self.to)

	def markRead(self):
		self.viewed=True
		self.save()

	def markAllRead(self, user):
		notifications = self.objects.filter(to=user)
		for n in notifications:
			n.viewed = True
			n.save()

	def dateSince(self):
		datePosted = self.theDate
		now = timezone.now()
		return now

class MassNotification(models.Model):
	title = models.CharField(max_length=400)
	text = models.TextField()
	theDate = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return '/notifications/public/%i/' % self.id

@receiver(post_save, sender=MassNotification)
def notifyInfo(**kwargs):
	bankingPeople = User.objects.all()
	print kwargs
	for i in bankingPeople:
		# if i.receiveInfo:
		Notification.objects.create(title='Incoming transaction!', level=1, to=i, text='sup')