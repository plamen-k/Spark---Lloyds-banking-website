# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns

urlpatterns = patterns("budget",
	url(r'^$', 'views.main', name='budget'),
	url(r'^setup$', 'views.monthly_budget_setup', name='monthly_budget_setup'),
	url(r'^add$', 'views.budget_add_purchase', name='budget_add_purchase'),
    url(r'^add_category$', 'views.add_category', name='add_category'),
    url(r'^past_budgets$', 'views.past_budgets', name='past_budgets'),
    url(r'^past_budgets/(?P<pk>[0-9]+)$', 'views.single_budget_view', name='single_budget_view'),
    url(r'^wishlist/(?P<pk>[0-9]+)$', 'views.wishlist', name='wishlist'),
    url(r'^create_wishlist_item$', 'views.create_wishlist_item', name='create_wishlist_item'),
	url(r'^get_saved_money$', 'views.get_saved_money', name='get_saved_money'),
	url(r'^mark_wishlist_purchased/(?P<pk>[0-9]+)', 'views.mark_wishlist_purchased', name='mark_wishlist_purchased'),


)
