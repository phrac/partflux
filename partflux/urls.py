from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = patterns('',
                       url(r'^$', 'partflux.views.index'),
                       url(r'^ajax/status/$', 'partflux.views.status_messages'),
                       url(r'^privacy/$', TemplateView.as_view(template_name="partflux/privacy.html")),
                       url(r'^parts/', include('parts.urls')),
                       url(r'^search/', include('search.urls')),
                       url(r'^companies/', include('companies.urls')),
                       url(r'^distributors/', include('distributors.urls')),
                       url(r'^select2/', include('django_select2.urls')),


                       # SITEMAP URLs
                       url(r'^sitemap.xml$', 'sitemap.index'),
                       url(r'^sitemap-(?P<sitemap_type>\w+)-(?P<sitemap_date>(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01]))-(?P<sitemap_page>\d+).xml', 'sitemap.sitemap'),

                       # Admin related urls
                       #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                      )
