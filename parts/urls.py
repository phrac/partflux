from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'parts.views.index'),
    url(r'^add/$', 'parts.views.addpartform'),
    url(r'^(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.detail'),
)
