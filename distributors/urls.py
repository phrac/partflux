from django.conf.urls import patterns, include, url
import distributors.click

urlpatterns = [
    url(r'^click/(?P<sku_id>\d+)/$', distributors.click.track_click),
]
