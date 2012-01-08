from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home'),
    
    url(r'^parts/$', 'parts.views.index'),
    url(r'^parts/(?P<part_id>\d+)/$', 'parts.views.detail'),
    url(r'^parts/search/$', 'parts.views.search'),

    url(r'^users/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'}),

    # activate admin stuff
    url(r'^admin/', include(admin.site.urls)),
)
