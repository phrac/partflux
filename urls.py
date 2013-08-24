from django.conf.urls import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib import admin
from tastypie.api import Api
from api import PartResource, AttributeResource, CompanyResource, UserResource

admin.autodiscover()

# setup the API urls
v1_api = Api(api_name='v1')
v1_api.register(PartResource())
v1_api.register(AttributeResource())
v1_api.register(CompanyResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^', include('main.urls')),
    
    # URLs for parts
    url(r'^parts/', include('parts.urls')),
    
    # URLs for search
    url(r'^search/', include('search.urls')),

    # URLs for companies
    url(r'^companies/', include('companies.urls')),
    #url('^faq/', include('faq.urls')),
    
    # URLs for users
    (r'^users/', include('users.urls')),

    # blog urls
    url(r'^blog/', include('blogango.urls')),

    # API URLs
    (r'^api/', include(v1_api.urls)),

    # URLS for distributors
    (r'^distributors/', include('distributors.urls')),
    
    
    # SITEMAP URLs
    url(r'^sitemap.xml$', 'sitemap.index'),
    url(r'^sitemap-(?P<sitemap_type>\w+)-(?P<sitemap_date>(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01]))-(?P<sitemap_page>\d+).xml', 'sitemap.sitemap'),

    # Admin related urls
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    )
