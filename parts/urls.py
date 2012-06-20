from django.conf.urls.defaults import patterns, include, url
from sitemap import PartSitemap

sitemaps = {
    'part': PartSitemap,
}

urlpatterns = patterns('',
    url(r'^$', 'parts.views.index'),
    url(r'^add/$', 'parts.views.addpartform'),
    url(r'^(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.detail'),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
