from django.template.loader import render_to_string
from django.shortcuts import render
from django.template import RequestContext
from datetime import date, timedelta, datetime
from django.template import loader, Context
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from parts.models import Part
from companies.models import Company
from nsn.models import Nsn

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
        obj = Part.objects.filter(created_at__range=(current_date, next_date))
    elif sitemap_type == 'companies':
        obj = Company.objects.filter(created_at__range=(current_date, next_date))
    elif sitemap_type == 'nsn':
        obj = Nsn.objects.filter(updated_at__range=(current_date, next_date))
        
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(obj, 500, request=request)
    try:
        obj_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        obj_list = p.page(1)    
    return render(request, 'sitemaps/sitemap.xml',
                 {'objects_list': obj_list,
                  'current_domain': 'http://partengine.org',
                 }, content_type='application/xml')

