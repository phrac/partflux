from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'companies.views.index'),
    url(r'^edit/(?P<company_slug>.+)/$', 'companies.views.edit'),
    url(r'^(?P<company_slug>.+)/$', 'companies.views.detail'),
)
