from django.conf.urls import include, url, patterns

urlpatterns = patterns('generator.views',

	url(r'create_super_user', 'createSuperUser', name='createSuperUser'),
	url(r'generate_outgoing', 'generateOutgoing', name='generateOutgoing'),
	url(r'generate_incoming', 'generateIncoming', name='generateIncoming'),
	
	url(r'generate_info_notification', 'generateInfoNotification', name='generateInfoNotification'),
	url(r'generate_success_notification', 'generateSuccessNotification', name='generateSuccessNotification'),
	url(r'generate_warning_notification', 'generateWarningNotification', name='generateWarningNotification'),
	url(r'generate_danger_notification', 'generateDangerNotification', name='generateDangerNotification'),
)