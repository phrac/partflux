from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User


from parts.models import Part, Xref
from partgroups.models import PartGroup
from companies.models import Company
from partgroups.forms import PartGroupForm


def index(request):
    partgroups = PartGroup.objects.filter(private=False)

    return render_to_response('partgroups/index.html',
                              {
                                  'partgroups': partgroups,
                              },
                              context_instance=RequestContext(request))


def detail(request, partgroup_id, slug):
    pg = get_object_or_404(PartGroup, pk=partgroup_id)

    return render_to_response('partgroups/detail.html',
                              {'partgroup': pg,
                              },
                              context_instance=RequestContext(request))


