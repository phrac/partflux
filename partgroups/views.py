from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.forms import ModelForm
from django.db import IntegrityError

from parts.models import Part, Xref
from partgroups.models import PartGroup, PartGroupItem
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
    partgroupform = PartGroupForm(instance=pg)
    return render_to_response('partgroups/detail.html',
                              {'partgroup': pg,
                               'partgroupform': partgroupform,
                              },
                              context_instance=RequestContext(request))

@login_required
def addgroupform(request):
    if request.method == 'POST':
        partgroupform = PartGroupForm(request.POST)
        if partgroupform.is_valid():
            name = partgroupform.cleaned_data['name']
            desc = partgroupform.cleaned_data['description']
            private = partgroupform.cleaned_data['private']
            partgroup = PartGroup(name=name, description=desc, private=private,
                                  user=request.user)
            try:
                partgroup.save()
            except IntegrityError:
                return HttpResponseBadRequest("Error creating new assembly")
                
            return HttpResponseRedirect(partgroup.get_absolute_url())
    else:
        partgroupform = PartGroupForm()
    return render_to_response('partgroups/add.html',
                              {'partgroupform': partgroupform,},
                              context_instance=RequestContext(request))


@login_required
def add_to_asm(request):
    if request.method == 'POST':
        asm_id = request.POST.get('asm_id', '')
        part_id = request.POST.get('part_id', '')
        asm = get_object_or_404(PartGroup, pk=asm_id)
        part = get_object_or_404(Part, pk=part_id)
        item = PartGroupItem(part=part, partgroup=asm, quantity=1, required=True)
        try:
            item.save()
        except IntegrityError:
            return HttpResponseBadRequest("Duplicate Part in Assembly")

        if request.is_ajax():
            return HttpResponse()
        else:
            return HttpResponseRedirect(asm.get_absolute_url())
    else:
        raise Http404
       

@login_required
def update_description(request):
    if request.method == 'POST':
        desc = request.POST.get('description', '')
        pg_id = request.POST.get('partgroup_id', '')
        pg = get_object_or_404(PartGroup, pk=pg_id)
        if request.user == pg.user:
            pg.description = desc
            pg.save()
            if request.is_ajax():
                return render_to_response('partgroups/includes/description.html',
                               {'partgroup': pg, },
                               context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('partgroups.views.detail',
                                                    args=[pg.id, pg.slug]))
        else:
            raise Http404
    else:
        raise Http404



