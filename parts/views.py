from amazon.api import AmazonAPI
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify, truncatechars, title
from partflux.templatetags import truncatesmart
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.contrib.sites.models import get_current_site
from django.db.models import Avg, Max, Min
from django.forms.formsets import formset_factory
from haystack.query import SearchQuerySet
import json
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from companies.models import Company
from parts.forms import NewPartForm, PropertyForm, XrefForm, ImageUploadForm, BuyLinkForm, ASINForm
from parts.models import Part, Attribute, Category
from distributors.models import Distributor, DistributorSKU
from distributors.forms import DistributorSKUForm

def index(request):
    parts = Part.objects.all().order_by('-updated_at')

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(parts, 25, request=request, reltuple=True )
    try:
        parts_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        parts_list = p.page(1)

    context = {'parts_list': parts_list,
               'page_num': page,
              }

    return render(request, 'parts/index.html', context)


def redirect_new_page(request, company_slug, part_slug):
    try:
        c = get_object_or_404(Company, slug=company_slug) 
        p = get_object_or_404(Part, slug=part_slug, company=c)
    except:
        p = get_object_or_404(Part, slug=part_slug)
        c = p.company
    return HttpResponsePermanentRedirect(reverse('parts.views.detail', args=[p.id, c.slug, p.slug]))

def redirect_sitemap(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    return HttpResponsePermanentRedirect(reverse('parts.views.detail',
                                                 args=[p.id, p.company.slug, p.slug]))
    
@login_required
def empty_category(response):
    from random import randint
    max_ = Part.objects.aggregate(Max('id'))['id__max']
    p = Part.objects.filter(id__gte=randint(1, max_))[0]

    return HttpResponseRedirect(reverse('parts.views.detail', args=[p.id, p.company.slug, p.slug]))
    
def detail(request, part_id, company_slug, part_slug):
    p = get_object_or_404(Part, id=part_id)
    
    pricing = DistributorSKU.objects.filter(part=p).aggregate(avg_price=Avg('price'), max_price=Max('price'), min_price=Min('price'))
    distributor_skus = DistributorSKU.objects.filter(part=p).order_by('price')
    current_site = get_current_site(request)
    page_title = "%s %s - %s" % (p.company.name, p.number,
                                    truncatesmart.truncatesmart(title(p.description),
                                    (settings.MAX_PAGE_TITLE_LENGTH
                                     - (len(p.number) +
                                     len(p.company.name)
                                     ))))

    PropertyFormSet = formset_factory(PropertyForm, extra=2, can_delete=True)
    forms = []
    tdict = {}
    for k, v in p.properties.items():
        forms.append({ 'key': k, 'value': v })
    property_formset = PropertyFormSet(initial=forms)

    xrefform = XrefForm(None)
    imageuploadform = ImageUploadForm(None)
    newskuform = DistributorSKUForm(None)
    asinform = ASINForm(None)

    if 'metadata_button' in request.POST:
        update_properties(request, p.id)

        if request.is_ajax():
            return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))

    if 'sku_button' in request.POST:
        newskuform = DistributorSKUForm(request.POST)
        if newskuform.is_valid():
            print 'valid'
            sku = newskuform.save(commit=False)
            sku.part = p
            sku.save()
                
            if request.is_ajax():
                return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))
        else:
            print 'Not valid'
            print newskuform.errors
    
    if 'description_button' in request.POST:
        description = request.POST.get('description', '')
        p.long_description = description
        p.save()
        if request.is_ajax():
            return render_to_response('parts/includes/long_description.html',
                                        {'part': p,},
                                    context_instance=RequestContext(request))

    if 'asin_button' in request.POST:
        asinform = ASINForm(request.POST)
        if asinform.is_valid():
            asin = asinform.cleaned_data['asin']
            p.asin = asin
            d = Distributor.objects.get(name='Amazon')
            amazon = AmazonAPI(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_ASSOCIATE_TAG)
            try:
                product = amazon.lookup(ItemId=asin)
            except:
                pass
            price = product.price_and_currency
            p.upc = product.upc
            p.ean = product.ean
            try:
                attrs = product.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height', 
                                                'ItemDimensions.Length', 'ItemDimensions.Weight'])
                print attrs
                weight = attrs['ItemDimensions.Weight']
                if not weight:
                    weight = product.get_attribute('Weight')
                p.weight = float(weight)/100.0
                print p.weight
                
            except:
                pass
            
            if not p.image_url or request.POST.get('replace_image', False):
                p.image_url = product.large_image_url
                
            p.save()
            ds = DistributorSKU(distributor=d, part=p, sku=asin, price=price[0],
                                url = product.offer_url)
            ds.save()
            p.save()
            
            if request.is_ajax():
                return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))

    	for c in p.cross_references.all():
	    c.categories.add(cat)
            
        if request.is_ajax():
            return render_to_response('parts/includes/category.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse('parts.views.detail',
                                                args=[part_id, p.company.slug, p.slug]))

    if 'xref_button' in request.POST:
        xrefform = XrefForm(request.POST)
        if xrefform.is_valid:
            status = addxref(request, p.pk)

            if request.is_ajax():
                return render_to_response('parts/includes/xrefs_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail',
                                                args=[part_id, p.company.slug, p.slug]))
            
    return render(request, 'parts/detail.html', {'part': p, 
            'property_formset': property_formset, 
            'xref_form' : xrefform,
            'imageuploadform' : imageuploadform,
            'newskuform' : newskuform,
            'page_title': page_title,
            'agg_pricing': pricing,
            'distributor_skus': distributor_skus,
            'asinform': asinform,
           })


@login_required
def update_properties(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    PropertyFormSet = formset_factory(PropertyForm)
    formset = PropertyFormSet(request.POST)
    new_properties = {}
    if formset.is_valid():
        for form in formset:
            if form.is_valid() and not form.empty_permitted:
                new_properties[form.cleaned_data['key']] = form.cleaned_data['value']
                
        print new_properties
        p.properties = new_properties
        p.save()
        return True
    else:
        return False

    
@login_required
def addbuylink(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    buylinkform = BuyLinkForm(request.POST)
    if buylinkform.is_valid():
        url = buylinkform.cleaned_data['url']
        company = buylinkform.cleaned_data['company'].strip().upper()
        price = buylinkform.cleaned_data['price']
        try:
            c = Company.objects.get(slug=slugify(company))
        except ObjectDoesNotExist:
            c = Company(name=company, slug=slugify(company))
            c.save()
        buylink = BuyLink(part=p, company=c, price=price, url=url, user=request.user)
        try:
            buylink.save()
            return True
        except IntegrityError:
            return 'Link already exists'


@login_required
def new_part(request):
    """Create a new part either by copying or from a blank form."""

    if request.method == 'POST':
        partform = NewPartForm(request.POST)
        if partform.is_valid():
            part = partform.save()
            return HttpResponseRedirect(part.get_absolute_url())
    else:
        copy = request.GET.get('copy', None)
        if copy:
            part = Part.objects.get(id=copy)
            partform = NewPartForm(instance=part)
        else:
            partform = NewPartForm()
    return render_to_response('parts/add.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))

@login_required
def addxref(request, part_id):
    """Add a cross reference to a part, also adding the part as a cross
    reference."""

    p = get_object_or_404(Part, pk=part_id)
    xrefform = XrefForm(request.POST)
    if xrefform.is_valid():
        form_part = xrefform.cleaned_data['part']
        copy_attrs = xrefform.cleaned_data['copy_attrs']

        p.cross_references.add(form_part)
        p.save()
        form_part.cross_references.add(p)
        form_part.save()
        return True
    else:
        return "Error"
            
