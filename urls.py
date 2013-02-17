from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib import admin
from tastypie.api import Api
from partfindr.api import PartResource, AttributeResource, CompanyResource, UserResource

from parts.feeds import LatestPartsFeed

admin.autodiscover()

# setup the API urls
v1_api = Api(api_name='v1')
v1_api.register(PartResource())
v1_api.register(AttributeResource())
v1_api.register(CompanyResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^', include('main.urls')),
    
    # RSS Feeds
    (r'^feeds/parts/latest/$', LatestPartsFeed()),
        
    # URLs for parts
    url(r'^parts/', include('parts.urls')),
    
    # URLs for comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # URLs for NSN
    url(r'^nsn/', include('nsn.urls')),
    
    # URLs for search
    url(r'^search/', include('search.urls')),

    # URLs for part groups
    url(r'^partgroups/', include('partgroups.urls')),
    
    # URLs for companies
    url(r'^companies/', include('companies.urls')),
    url('^faq/', include('faq.urls')),
    
    # URLs for users
    
    (r'^users/', include('users.urls')),

    # API URLs
    (r'^api/', include(v1_api.urls)),

    # SITEMAP URLs
    url(r'^sitemap.xml$', 'sitemap.index'),
    url(r'^sitemap-(?P<sitemap_date>(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01])).xml', 'sitemap.sitemap'),

    # Admin related urls
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    )
