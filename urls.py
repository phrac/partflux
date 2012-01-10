from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.comingsoon'),
    
    url(r'^parts/$', 'parts.views.index'),
    url(r'^parts/(?P<part_id>\d+)/$', 'parts.views.detail'),
    url(r'^parts/search/$', 'parts.views.search'),
    #url(r'^parts/addmeta/(?P<part_id>\d+)/$', 'parts.views.addmeta'),
    #url(r'^parts/addxref/(?P<part_id>\d+)/$', 'parts.views.addxref'),

    url(r'^companies/$', 'companies.views.index'),
    url(r'^companies/(?P<company_id>\d+)/$', 'companies.views.detail'),

    (r'^users/', include('registration.backends.default.urls')),

    # activate admin stuff
    url(r'^admin/', include(admin.site.urls)),
)
