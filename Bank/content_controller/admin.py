# Code written by Plamen Kolev

from django.contrib import admin
from content_controller.models import Slide, Service, UserStory
# Register your models here.

class SlideAdmin(admin.ModelAdmin):
	list_display = ('title', 'display_image', 'display')

class ServiceAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug' : ('title',)}


admin.site.register(Slide, SlideAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(UserStory,)
