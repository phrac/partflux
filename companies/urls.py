from django.conf.urls import patterns, include, url
import companies.views

urlpatterns = [
    url(r'^$', companies.views.index),
    url(r'^edit/(?P<company_id>\d+)/(?P<company_slug>.+)/$', companies.views.edit),
    url(r'^(?P<company_id>\d+)/(?P<company_slug>.+)/$', companies.views.detail),
    url(r'^(?P<company_slug>.+)/$', companies.views.redirect_new_page),
]
