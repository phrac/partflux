from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^click/(?P<sku_id>\d+)/$', 'distributors.click.track_click'),
    )
