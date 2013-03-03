from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'partgroups.views.index'),
                        
    url(r'^add/$', 'partgroups.views.addgroupform'),
    url(r'^add_to_asm', 'partgroups.views.add_to_asm'),
    url(r'^update_desc', 'partgroups.views.update_description'),
    url(r'^(?P<partgroup_id>\d+)/(?P<slug>.+)/$', 'partgroups.views.detail'),

)
