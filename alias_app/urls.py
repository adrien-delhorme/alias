from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^', include('alias_app.webapp.urls')),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
