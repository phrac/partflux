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
    return render_to_response('search/results.html',
                              {},
                              context_instance=RequestContext(request))

