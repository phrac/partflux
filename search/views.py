from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User


from parts.models import Part, Xref
from companies.models import Company
from parts.forms import SearchForm


def index(request):
    parts_list = Part.objects.all().order_by('-created_at')[:20]
    paginator = Paginator(parts_list, 20)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        parts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        parts = paginator.page(paginator.num_pages)

    return render_to_response('search/index.html',
                           {},
                           context_instance=RequestContext(request))


def results(request):
    searchform = SearchForm(request.GET)
    
    if searchform.is_valid():
        q = searchform.cleaned_data['q']
        if q:
            results = Part.objects.filter(Q(number__istartswith=q) |
                                          Q(tsv__query=q)).distinct().only('number', 'description', 'company')
        else:
            results = []
    
        try:                                                                    
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(results, 20, request=request)
        parts_list = p.page(page)
    
    return render_to_response('search/results.html',
                              { 
                                  'parts_list': parts_list, 
                                  'searchterm': q,
                              },
                              context_instance=RequestContext(request))
