from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'alias_app.webapp.views.home_view', name='home'),
    url(r'^wizard/$', 'alias_app.webapp.views.wizard_view', name='wizard'),
    url(r'^setup/$', 'alias_app.webapp.views.setup_view', name='setup'),
    url(r'^list/$', 'alias_app.webapp.views.alias_list_view', name='alias-list'),
    url(r'^delete/(?P<resource_id>\d+)/$', 'alias_app.webapp.views.alias_delete_view', name='alias-delete'),
)
