from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home'),
	url(r'^parts/$', 'parts.views.index'),
	url(r'^parts/(?P<part_id>\d+)/$', 'parts.views.detail'),
	url(r'^parts/search/$', 'parts.views.search'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
