# Code written by Plamen Kolev

from django.conf.urls import include, url, patterns

urlpatterns = patterns('userprofile.views',

    url(r'^$', 'viewProfile', name='viewProfile'),
    url(r'^settings/$', 'changeSettings', name='changeSettings'),   
    url(r'^lock/$', 'lock', name='lock_account'),

    url(r'^branch_finder','branch_finder', name='branch_finder'),

    url(r'student_account$', 'student_account', name='student_account'),
    url(r'graduate_account$', 'graduate_account', name='graduate_account'),
    url(r'budgeting_info', 'budgeting_info', name='budgeting_info'),
    url(r'legal', 'legal', name='legal'),
    # link the index page with the account view for now, 90% will change later
    # url(r'^settings/change_password$', 'change_password', name='change_password'),

)