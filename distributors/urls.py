from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'companies.views.index'),
    url(r'^add/$', 'distributors.views.new_sku'),
    )
