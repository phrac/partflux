from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'nsn.views.index'),
    url(r'^(?P<nsn_id>\d+)/(?P<nsn_number>.+)/$', 'nsn.views.detail'),
    

)