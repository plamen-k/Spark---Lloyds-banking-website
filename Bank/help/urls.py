# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns

urlpatterns = patterns("help",
    url(r'^$', 'views.help_main', name='help_main'),
	# url(r'^ask$', 'views.ask_question', name='ask_question'),

	# api

)
