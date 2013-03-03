from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Uncomment the below URL to disable users section                   
    #url(r'^users/.*', 'django.views.generic.simple.direct_to_template',
    #    {'template': 'users/disabled.html'}),
    url(r'^$', 'users.views.index'),

    url(r'^logout/$',
       auth_views.logout,
       {'next_page': '/'}),

    url(r'^profile/([a-zA-Z0-9]+)/$', 'users.views.view_profile'),
    
    url(r'^favorites/$', 'users.views.view_favorites'),
    url(r'^favorites/edit_notes/$', 'users.views.edit_favorite_notes'),
    
    url(r'^password/reset/$',
       auth_views.password_reset,
       {'template_name': 'registration/pwreset.html'}
      ),
    
    (r'^', include('registration.urls')),
)
