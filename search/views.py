from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.template import RequestContext
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery

from parts.models import Part
from companies.models import Company
from search.forms import SearchForm
import urllib
import re

def index(request):
    return render_to_response('search/index.html',
                              {},
                              context_instance=RequestContext(request))


def results(request):
    url = urllib.unquote_plus(request.get_full_path())
    print url
    searchform = SearchForm(request.GET)
    
    if not "q" in request.GET:
        return redirect('search.views.index')
    
    if searchform.is_valid():
        q = searchform.cleaned_data['q']
        selected_facets = request.GET.getlist("selected_facets")
        remove_facets = request.GET.getlist("remove_facets")
        applied_facets = {}
        
        if remove_facets:
            for r in remove_facets:
                filter(lambda a: a != r, selected_facets)
                filter(lambda a: a != r, applied_facets)

        if selected_facets:
            for f in selected_facets:
                k, v = f.split(":")
                myurl = url.replace("&selected_facets=%s" % f, "")
                tag = "%s : %s" % (k.upper(), v)
                applied_facets[tag] = myurl 
                print applied_facets
        

        if q:
            sqs = SearchQuerySet().models(Part).models(Company).facet('brand').facet('category').facet('with_distributors').facet('with_image').auto_query(q)
            
            for facet in selected_facets:
                sqs = sqs.narrow(facet)

        try:                                                                    
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(sqs, 10, request=request)
        results_list = p.page(page)

    return render_to_response('search/results.html',
                              { 
                                  'results_list': results_list, 
                                  'query': q,
                                  'facets': sqs.facet_counts(),
                                  'applied_facets': applied_facets,
                              },
                              context_instance=RequestContext(request))

