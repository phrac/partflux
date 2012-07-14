from django.template.loader import render_to_string
from django.shortcuts import render
from django.template import RequestContext
from datetime import date, timedelta, datetime
from django.template import loader, Context

from parts.models import Part
from companies.models import Company

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
    

def sitemap(sitemap_date):
    current_date = datetime.strptime(sitemap_date, '%Y-%m-%d')
    next_date = current_date + timedelta(hours=24)
    parts = Part.objects.filter(created_at__range=(current_date, next_date))[:50000]
    filename = "/home/derek/web/static/sitemaps/sitemap-parts-%s.xml" % sitemap_date
    open(filename, "w").write(render_to_string('sitemaps/sitemap.xml', {'objects': parts, 'current_domain' : 'http://partengine.org'}))
    companies = Company.objects.filter(created_at__range=(current_date, next_date))
    print "wrote %s" % filename
    filename = "/home/derek/web/static/sitemaps/sitemap-companies-%s.xml" % sitemap_date
    open(filename, "w").write(render_to_string('sitemaps/sitemap.xml', {'objects': companies, 'current_domain' : 'http://partengine.org'}))
    print "wrote %s" % filename

