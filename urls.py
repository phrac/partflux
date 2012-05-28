from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = patterns('',
                       
                       #GENERIC VIEWS
                       url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main/comingsoon.html'}),
                       #url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main/index.html'}), 
                       
                       url(r'^partbot/$',
                           'django.views.generic.simple.direct_to_template',
                           {'template': 'main/partbot.html'}),
                       
                       url(r'^about/$', 
                           'django.views.generic.simple.direct_to_template', 
                           {'template': 'main/about.html'}),

                       url(r'^contact/$',
                           'django.views.generic.simple.direct_to_template',
                           {'template': 'main/contact.html'}),
                      
                       # URLs for parts
                       url(r'^parts/$', 'parts.views.index'),
                       url(r'^parts/add/$', 'parts.views.addpart'),
                       url(r'^parts/(?P<part_id>[a-z0-9]+)/$', 'parts.views.detail'),
                       
                       
                       # URLs for NSN
                       #url(r'^nsn/$', 'nsn.views.index'),
                       #url(r'^nsn/(?P<nsn_id>\d+)/.*$', 'nsn.views.detail'),
                       
                       # URLs for search
                       url(r'^search/advanced/$', 'search.views.index'),
                       url(r'^search/', 'search.views.results'),
                       #(r'^search/', include('haystack.urls')),

                       # URLs for part groups
                       url(r'^partgroups/$', 'partgroups.views.index'),
                       url(r'^partgroups/(?P<partgroup_id>\d+)/$', 'partgroups.views.detail'), 
                       
                       # URLs for companies
                       url(r'^companies/$', 'companies.views.index'),
                       url(r'^companies/(?P<company_id>\d+)/$',
                           'companies.views.detail'),
                       
                       # URLs for comments
                       (r'^comments/', include('django.contrib.comments.urls')),

                       # URLs for users
                       url(r'^users/logout/$',
                           auth_views.logout,
                           {'template_name': 'main/comingsoon.html'}),
                       
                       url(r'^users/password/reset/$',
                           auth_views.password_reset,
                           {'template_name': 'registration/pwreset.html'}
                          ),

                       (r'^users/', include('registration.backends.default.urls')),
                       
                      )
