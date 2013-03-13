from django.shortcuts import render
from datetime import date, timedelta, datetime
from haystack.query import SearchQuerySet

from parts.models import Part
from companies.models import Company
from nsn.models import Nsn


def index(request):
    start = date(2012, 1, 1)
    end = date.today() - timedelta(days=1)
    delta = end - start
    date_list = [ end - timedelta(days=x) for x in range(0, delta.days) ]

    return render(request, 'sitemaps/index.xml',
                  { 'dates': date_list },
                  content_type='application/xml')
    

def sitemap(request, sitemap_type, sitemap_date):
    current_date = datetime.strptime(sitemap_date, '%Y-%m-%d')
    next_date = current_date + timedelta(hours=24)
    if sitemap_type == 'parts':
        results = SearchQuerySet().filter(created__range=[current_date,
                                                           next_date]).models(Part).values('url')[:50000]
    elif sitemap_type == 'companies':
        results = SearchQuerySet().filter(created__range=[current_date,
                                                           next_date]).models(Company).values('url')[:50000]
    elif sitemap_type == 'nsn':
        results = SearchQuerySet().filter(created__range=[current_date,
                                                           next_date]).models(Nsn).values('url')[:50000] 
    return render(request, 'sitemaps/sitemap.xml',
                 {'objects_list': results,
                  'type': sitemap_type,
                  'current_domain': 'http://partengine.org',
                 }, content_type='application/xml')


