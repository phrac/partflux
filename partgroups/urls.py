from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'partgroups.views.index'),
    url(r'^(?P<partgroup_id>\d+)/(?P<slug>.+)/$', 'partgroups.views.detail'),

)
