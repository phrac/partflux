from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from companies.models import Company

def index(request):
    companies_list = Part.objects.all().order_by('created_at')
    paginator = Paginator(parts_list, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        companies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        companies = paginator.page(paginator.num_pages)

    return render_to_response('companies/index.html', 
                              {'companies_list': companies}, 
                              context_instance=RequestContext(request))

def detail(request, company_id):
     c = get_object_or_404(Company, pk=company_id)
     
     return render_to_response('companies/detail.html',
                                {'company': c},
                                context_instance=RequestContext(request))

