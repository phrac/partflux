from django.conf.urls.defaults import patterns, include, url
from sitemap import PartSitemap
from parts.feeds import LatestPartsFeed

urlpatterns = patterns('',
    url(r'^$', 'parts.views.index'),
    
    url(r'^add/$', 'parts.views.addpartform'),

    url(r'^ajax/description/$', 'parts.ajax.update_description'),
    
    url(r'^(?P<part_id>\d+)/(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.detail'),
    url(r'^(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.redirect_new_page'),
    

)
