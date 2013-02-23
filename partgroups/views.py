from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.forms import ModelForm


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
            partgroup.save()
            return HttpResponseRedirect(partgroup.get_absolute_url())
    else:
        partgroupform = PartGroupForm()
    return render_to_response('partgroups/add.html',
                              {'partgroupform': partgroupform,},
                              context_instance=RequestContext(request))

@login_required
def update_description(request):
    if request.method == 'POST':
        desc = request.POST.get('description', '')
        print desc
        pg_id = request.POST.get('partgroup_id', '')
        print pg_id
        pg = get_object_or_404(PartGroup, pk=pg_id)
        print '1'
        if request.user == pg.user:
            print '2'
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



