from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^ajax/status/$', 'main.views.status_messages'), 
    
    url(r'^partbot/$',
       'django.views.generic.simple.direct_to_template',
       {'template': 'main/partbot.html'}),
    
    url(r'^privacy/$',
       'django.views.generic.simple.direct_to_template',
       {'template': 'main/privacy.html'}),
       
    url(r'^contest/$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'main/contest.html'}),
)
