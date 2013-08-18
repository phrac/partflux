from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^ajax/status/$', 'main.views.status_messages'), 
    
    #url(r'^partbot/$',
    #   'django.views.generic.simple.direct_to_template',
    #   {'template': 'main/partbot.html'}),
    
    url(r'^privacy/$', TemplateView.as_view(template_name="main/privacy.html")),
              
)
