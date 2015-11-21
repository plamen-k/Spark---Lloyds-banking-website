# Code written by Plamen Kolev

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_delete, pre_save	
from django.dispatch.dispatcher import receiver
from tinymce.models import HTMLField
from django.template.defaultfilters import slugify

# Create your models here.
class Slide(models.Model):
	title = models.CharField(max_length=200)
	image = models.ImageField(upload_to = "slider", null=False, blank=False)
	dateUploaded = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
	display = models.BooleanField(default=True)
	
	def display_image(self):
		return mark_safe("<img height='200' src='/media/%s'>" % self.image)
	display_image.allow_tags = True



class Service(models.Model):
	CHOICES = (
		('plus', "Plus"),
		('ok', "Ok"),
		('home', "Home"),
		('gbp', "Pound"),
		('send', "Send"),
		('earphone', "Phone"),
	)
	thumbnail = models.CharField(max_length=30, choices=CHOICES, default='ok')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=300)
	body = HTMLField()
	dateUploaded = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
	display = models.BooleanField(default=True)

	def __str__(self):
		return self.title

class UserStory(models.Model):
	name = models.CharField(max_length = 200)
	image = models.ImageField(upload_to = "slider", null=False, blank=False)
	slug = models.SlugField(max_length=300)
	title = models.CharField(max_length=200)
	body = HTMLField()
	dateUploaded = models.DateTimeField(auto_now=True, auto_now_add=False, default=timezone.now())
	display = models.BooleanField(default=True)

	def __str__(self):
		return self.name

@receiver(pre_delete, sender=Slide)
def slide_delete(sender, instance, **kwargs):
	if(instance.image is not None):
		instance.image.delete(False)
	else:
		return "error"

@receiver(pre_delete, sender=UserStory)
def slide_delete(sender, instance, **kwargs):
	if(instance.image is not None):
		instance.image.delete(False)
	else:
		return "error"

@receiver(pre_save, sender=Service)
def generateSlug(sender,instance, **kwargs):
	instance.slug = slugify(instance.title)

@receiver(pre_save, sender=UserStory)
def generateSlug(sender,instance, **kwargs):
	instance.slug = slugify(instance.name)

