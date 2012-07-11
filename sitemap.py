from django.shortcuts import render
from django.template import RequestContext
from datetime import date, timedelta, datetime

from parts.models import Part

def index(request):
    START_DATE = date(2012, 1, 1)
    END_DATE = date.today()
    td = datetime.timedelta(hours=24)
    current_date = END_DATE
    datelist = []
    while current_date >= START_DATE:
        datelist.append(current_date)
        current_date -= td

    return render(request, 'sitemaps/index.xml',
                  { 'dates': datelist },
                  content_type='application/xml')
    

def sitemap(request, sitemap_date):
    date_object = datetime.strptime(sitemap_date, '%Y-%m-%d')
    next_date = date_object + timedelta(hours=24)
    parts = Part.objects.filter(created_at__range=(date_object, next_date))

    return render(request, 'sitemaps/sitemap.xml',
                  { 'parts' : parts },
                  content_type='application/xml')
