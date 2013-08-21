from django.shortcuts import render
from datetime import date, timedelta, datetime
from haystack.query import SearchQuerySet

from parts.models import Part
from companies.models import Company
import math

def index(request):
    start = date(2012, 1, 1)
    date_list = []
    end = date.today() - timedelta(days=1)
    delta = end - start
    for x in range(0, delta.days):
        urldict = {}
        today = end - timedelta(days=x)
        current_date = today
        next_date = current_date + timedelta(hours=24)
        count = SearchQuerySet().filter(created__range=[current_date, next_date]).count()
        if count > 0:
            num_pages = int(math.ceil(count/10000.0))
            for x in range(0, num_pages):
                urldict[x] = today
            date_list.append(urldict)

    return render(request, 'sitemaps/index.xml',
                  { 'dates': date_list },
                  content_type='application/xml')
    

def sitemap(request, sitemap_type, sitemap_date, sitemap_page):
    limit = 10000
    offset = (int(sitemap_page) * limit)
    new_limit = offset+limit
    current_date = datetime.strptime(sitemap_date, '%Y-%m-%d')
    next_date = current_date + timedelta(hours=24)
    if sitemap_type == 'parts':
        results = SearchQuerySet().filter(created__range=[current_date,
                                                           next_date]).models(Part).values('url')[offset:new_limit]
    elif sitemap_type == 'companies':
        results = SearchQuerySet().filter(created__range=[current_date,
                                                           next_date]).models(Company).values('url')[:50000]
    return render(request, 'sitemaps/sitemap.xml',
                 {'objects_list': results,
                  'type': sitemap_type,
                  'current_domain': 'http://partflux.com',
                 }, content_type='application/xml')


