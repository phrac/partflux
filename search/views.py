from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core import serializers
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django.conf import settings

from pyes import *
from parts.models import Part, Xref
from companies.models import Company
from search.forms import SearchForm

def index(request):
    return render_to_response('search/index.html',
                              {},
                              context_instance=RequestContext(request))

def results(request):

    NUM_RESULTS = 20
    conn = ES(settings.ES_HOST)
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return redirect('search.views.index')
    else:
        q = request.GET['q']

    if searchform.is_valid():
        query = StringQuery(q,
                            default_operator="AND",
                            search_fields=['number', 
                                           'company', 
                                           'desc',
                                           'attrstring',],
                           )
        s = Search(query, fields=['pgid'], size=500)
        raw_results = conn.search(s)

        results = []
        for r in raw_results:
            if r.pgid is not None:
                results.append(Part.objects.get(pk=r.pgid))
            else:
                pass

        if "page" in request.GET:                                                                    
            page = request.GET.get('page', 1)
        else:
            page = 1

        p = Paginator(results, NUM_RESULTS, request=request)
        try:
            results_list = p.page(page)
        except (PageNotAnInteger, EmptyPage):
            results_list = p.page(1)

    return render_to_response('search/results.html',
                              { 
                                  'results_list': results_list, 
                                  'searchterm': q,
                              },
                              context_instance=RequestContext(request))

