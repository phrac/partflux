from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

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
    conn = ES('127.0.0.1:9200')
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return redirect('search.views.index')
    else:
        q = request.GET['q']

    if searchform.is_valid():
        query = TextQuery('fulltext', q, operator='and')
        
        s = Search(query, fields=['pgid'], size=250)
        raw_results = conn.search(s)

        results = []
        for r in raw_results:
            results.append(Part.objects.get(pk=r.pgid))

        try:                                                                    
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(results, NUM_RESULTS, request=request)
        results_list = p.page(page)

    return render_to_response('search/results.html',
                              { 
                                  'results_list': results_list, 
                                  'searchterm': q,
                              },
                              context_instance=RequestContext(request))