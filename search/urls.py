from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^advanced/$', 'search.views.index'),
    url(r'^autocomplete/$', 'search.views.autocomplete'),
    url(r'^$', 'search.views.results'),
)