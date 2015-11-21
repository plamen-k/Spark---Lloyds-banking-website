# Code written by Plamen Kolev


from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',

    url(r'^$','Bank.views.index', name='index'),
    # link the index page with the account view for now, 90% will change later
    url(r'^testhtml$','Bank.views.testHtml', name='testHtml'),
    # link the index page with the account view for now, 90% will change later
    url(r'^payment/', include('payment.urls')),
    # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    url(r'^info/', include('userprofile.urls')),
    # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    url(r'^generator/', include('generator.urls')),
    # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    url(r'^admin/', include(admin.site.urls)),
    # default django admin
    url(r'^notifications/', include('notification.urls')),
    # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    url(r'^help/', include('help.urls')),
    # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    #urlconf for the content_controller
    url(r'^profile/', include('content_controller.urls')), # this is a redirect to the url config inside the account app, look inside account.urls for the mapping
    url(r'^budget/', include('budget.urls')),
    # the login and logout use the default django contrib authentication system (for more details view the admin panel under auth, thats where it gets it's hooks)
    # it is customizable, for example here we pass the template where we have minimal code to just render the username and massword, name is used for indication for action="?" in forms that require login, aka form loopback
    url(r'^login/$', 'django.contrib.auth.views.login',  {'template_name': 'payment/login.html'}, name="my_login"),
    #  the next_page argument just sends you to the homepage after you log in, otherwise you get the default django login auth
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),

    url('^change-password/', 'django.contrib.auth.views.password_change', name="change_password"),
    url(r'^password/changed$', 'django.contrib.auth.views.password_change', {'password_change_done': '/settings/users/password-changed'}),
    url(r'^user/password_change/done/$', 'django.contrib.auth.views.password_change_done', name="password_change_done"),

     url(r'^api/', include('api.urls')), # this is a redirect to the url config inside the account app, look inside account.urls for the mapping

    (r'^tinymce/', include('tinymce.urls')), # for tiny mce (rich text field)
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns) # enables restful api functionality (wrapper)
