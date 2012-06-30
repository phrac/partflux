from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    #GENERIC VIEWS
    #url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'main/comingsoon.html'}),
    
    url(r'^', include('main.urls')),
    
    # URLs for parts
    url(r'^parts/', include('parts.urls')),
    
    # URLs for comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # URLs for NSN
    #url(r'^nsn/$', 'nsn.views.index'),
    #url(r'^nsn/(?P<nsn_id>\d+)/.*$', 'nsn.views.detail'),
    
    # URLs for search
    url(r'^search/', include('search.urls')),
    
    # URLs for part groups
    url(r'^partgroups/$', 'partgroups.views.index'),
    url(r'^partgroups/(?P<partgroup_id>\d+)/$', 'partgroups.views.detail'), 
    
    # URLs for companies
    url(r'^companies/', include('companies.urls')),
    url('^faq/', include('faq.urls')),
    
    # URLs for users
    
    # Uncomment the below URL to disable users section                   
    #url(r'^users/.*', 'django.views.generic.simple.direct_to_template',
    #    {'template': 'users/disabled.html'}),

    url(r'^users/logout/$',
       auth_views.logout,
       {'next_page': '/'}),
    
    url(r'^users/password/reset/$',
       auth_views.password_reset,
       {'template_name': 'registration/pwreset.html'}
      ),
    
    (r'^users/', include('registration.urls')),

    # Admin related urls
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    )
