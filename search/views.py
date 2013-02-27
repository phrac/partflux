from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from parts.models import Part, Xref
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
        no_partial_q = re.sub('\{.+\}', '', q)
        no_partial_q = re.sub('\(.+\)', '', no_partial_q)
        no_partial_q = re.sub('\[.+\]', '', no_partial_q)

        selected_facets = request.GET.getlist("f")
        
        partial = re.findall(r'\{(.+?)\}', q)
        company = re.findall(r'\((.+?)\)', q)
        nsn = re.findall(r'\[(.+?)\]', q)

        if q:
            sqs = SearchQuerySet()
            results = sqs.filter(content=AutoQuery(no_partial_q))[:250]

            # check for a partial part number search
            if partial:
                firsthit = str(partial[0])
                if results:
                    results = results.narrow(u'number:"%s"' % firsthit)
                else:
                    results = sqs.filter(number__contains=firsthit)
            if company:
                firsthit = str(company[0])
                if results:
                    results = results.narrow(u'company:"%s"' % firsthit)
                else:
                    results = sqs.filter(company__contains=firsthit)


        else:
            results = []

        # drill down
        for facet in selected_facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)

            if value:
                results = results.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

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
                                 # 'facets': results.facet_counts(),
                              },
                              context_instance=RequestContext(request))

