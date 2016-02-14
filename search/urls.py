from django.conf.urls import patterns, include, url
import search.views
import search.autocomplete

urlpatterns = [
    #url(r'^$', include('haystack.urls')),
    url(r'^advanced/$', search.views.index),
    url(r'^autocomplete/$', search.autocomplete.autocomplete),
    url(r'^$', search.views.results),
]
