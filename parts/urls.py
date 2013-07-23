from django.conf.urls.defaults import patterns, include, url
from sitemap import PartSitemap
from parts.feeds import LatestPartsFeed

urlpatterns = patterns('',
    url(r'^$', 'parts.views.index'),
    
    url(r'^add/$', 'parts.views.addpartform'),
    url(r'^spree/$', 'parts.views.empty_category'),

    url(r'^ajax/description/$', 'parts.ajax.update_description'),
    url(r'^ajax/update_company/$', 'parts.ajax.update_company'),
    url(r'^ajax/load_distributors/(\d+)/$', 'parts.ajax.get_distributors'),
    url(r'^ajax/load_images/(\d+)/$', 'parts.ajax.get_images'),
    url(r'^ajax/asin_search/(\d+)/$', 'parts.ajax.admin_asin_search'),
    url(r'^ajax/flag/$', 'parts.ajax.flag'),
    
    url(r'^ajax/add_favorite/$', 'parts.ajax.add_favorite'),
    
    url(r'^ajax/delete_favorite/$', 'parts.ajax.delete_favorite'),
    url(r'^ajax/delete_buylink/(\d+)/$', 'parts.ajax.delete_buylink'),
    url(r'^ajax/delete_image/$', 'parts.ajax.delete_image'),
    url(r'^ajax/parent_categories/$', 'parts.ajax.get_parent_categories'),
    url(r'^ajax/child_categories/(\d+)/$', 'parts.ajax.get_child_categories'),

    url(r'^(?P<part_id>\d+)/(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.detail'),
    url(r'^(?P<part_id>\d+)/$', 'parts.views.redirect_sitemap'),
    url(r'^(?P<company_slug>.+)/(?P<part_slug>.+)/$', 'parts.views.redirect_new_page'),

)
