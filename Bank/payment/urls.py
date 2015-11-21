# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns

urlpatterns = patterns("payment",
    url(r'^send/$', 'views.sendMoney', name='sendMoney'),
    url(r'^statement/(?P<pk>\d+)$', 'views.statement', name='statement'),
    url(r'^account/rename/(?P<pk>\d+)$', 'views.change_account_name', name='change_account_name'),
    url(r'^save_to_payee$', 'views.save_to_payee', name='save_to_payee'),

    # api

)
