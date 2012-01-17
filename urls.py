from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.comingsoon'),
    
    # URLs for parts
    url(r'^parts/$', 'parts.views.index'),
    url(r'^parts/(?P<part_id>\d+)/.*$', 'parts.views.detail'),
    
    # URLs for search
    url(r'^search/$', 'search.views.index'),
    url(r'^search/results/$', 'search.views.results'),

    # URLs for companies
    url(r'^companies/$', 'companies.views.index'),
    url(r'^companies/(?P<company_id>\d+)/$', 'companies.views.detail'),

    # URLs for users
    (r'^users/', include('registration.backends.default.urls')),

    # activate admin stuff
    url(r'^admin/', include(admin.site.urls)),
)
