# Code written by Plamen Kolev

from django.contrib import admin
from .models import Notification, MassNotification

class NotificationAdmin(admin.ModelAdmin):
	list_display = ("title", 'viewed', 'read', 'theDate')

admin.site.register(Notification, NotificationAdmin)
admin.site.register(MassNotification,)