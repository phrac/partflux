from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from parts.models import Part
from companies.models import Company
from search.forms import SearchForm

import re

def index(request):
    return render_to_response('search/index.html',
                              {},
                              context_instance=RequestContext(request))


def results(request):
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return redirect('search.views.index')
    
    if searchform.is_valid():
        q = searchform.cleaned_data['q']

        if q:
            sqs = SearchQuerySet().auto_query(q)
            suggestions = sqs.spelling_suggestion()
            results = sqs.filter(content=AutoQuery(q))[:250]

        else:
            results = []

        try:                                                                    
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(results, 20, request=request)
        results_list = p.page(page)

    return render_to_response('search/results.html',
                              { 
                                  'results_list': results_list, 
                                  'searchterm': q,
                                  'sqs': sqs,
                                  'suggestions': suggestions,
                                 # 'facets': results.facet_counts(),
                              },
                              context_instance=RequestContext(request))

