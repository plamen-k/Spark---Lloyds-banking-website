# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns

urlpatterns = patterns("content_controller.views",
    url(r'service/(?P<slug>[-\w]+)$', 'service', name='service'),
    url(r'story/(?P<slug>[-\w]+)$', 'story', name='story'),


)