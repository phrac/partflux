from django.template.loader import render_to_string
from django.shortcuts import render
from django.template import RequestContext
from datetime import date, timedelta, datetime
from django.template import loader, Context
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from haystack.query import SearchQuerySet

from parts.models import Part
from companies.models import Company
from nsn.models import Nsn

LINKS_PER_PAGE = 1000

def index(request):
    START_DATE = date(2012, 1, 1)
    END_DATE = date.today() - timedelta(hours=24)
    td = timedelta(hours=24)
    current_date = END_DATE
    datelist = []
    while current_date >= START_DATE:
        datelist.append(current_date)
        current_date -= td

    return render(request, 'sitemaps/index.xml',
                  { 'dates': datelist },
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


