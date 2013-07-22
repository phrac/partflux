from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify, truncatechars
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.contrib.sites.models import get_current_site
from django.db.models import Avg, Max, Min
from haystack.query import SearchQuerySet
import json
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from companies.models import Company
from parts.forms import MetadataForm, XrefForm, ImageUploadForm, BuyLinkForm, ASINForm
from parts.models import Part, PartImage, Attribute, Category
from distributors.models import Distributor, DistributorSKU

def index(request):
    parts = Part.objects.all().order_by('-created_at')

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(parts, 25, request=request, reltuple=True )
    try:
        parts_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        parts_list = p.page(1)

    return render_to_response('parts/index.html',
                              {'parts_list': parts_list,
                               'page_num': page,
                              },
                              context_instance=RequestContext(request))


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
    parts = Part.objects.filter(categories=None).order_by('?')[:1]
    p = parts[0]
    return HttpResponseRedirect(reverse('parts.views.detail', args=[p.id, p.company.slug, p.slug]))
    
def detail(request, part_id, company_slug, part_slug):
    p = get_object_or_404(Part, id=part_id)
    mlt = SearchQuerySet().models(Part).more_like_this(p)[:10]
    pricing = DistributorSKU.objects.filter(part=p).aggregate(avg_price=Avg('price'), max_price=Max('price'), min_price=Min('price'))
    distributor_skus = DistributorSKU.objects.filter(part=p)
    current_site = get_current_site(request)
    title = "%s by %s - %s | %s" % (p.number, p.company.name,
                                    truncatechars(p.description,
                                    (settings.MAX_PAGE_TITLE_LENGTH
                                     - (len(p.number) +
                                     len(p.company.name)
                                     + 22))),
                                    current_site.name)

    metaform = MetadataForm(None)
    xrefform = XrefForm(None)
    imageuploadform = ImageUploadForm(None)
    buylinkform = BuyLinkForm(None)
    asinform = ASINForm(None)

    if 'buylink_button' in request.POST:
        buylinkform = BuyLinkForm(request.POST)
        if buylinkform.is_valid:
            status = addbuylink(request, p.pk)

            if request.is_ajax():
                return render_to_response('parts/includes/buylink_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail', args=[part_id, p.company.slug, p.slug]))

    if 'metadata_button' in request.POST:
        metaform = MetadataForm(request.POST)
        if metaform.is_valid:
            status, new_id = addmeta(request, p.pk)
                
            if request.is_ajax():
                return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))
    if 'asin_button' in request.POST:
        asinform = ASINForm(request.POST)
        if asinform.is_valid():
            asin = asinform.cleaned_data['asin']
	    p.asin = asin
            p.save()
	    for x in p.cross_references.all():
	        x.asin = asin
	        x.save()
                
            if request.is_ajax():
                return render_to_response('parts/includes/attribute_table.html',
                                          {'part': p,},
                                          context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))

    if 'category_button' in request.POST:

        cat1 = request.POST.get('cat1', None)
        cat2 = request.POST.get('cat2', None)
        cat3 = request.POST.get('cat3', None)
        cat4 = request.POST.get('cat4', None)
        cat5 = request.POST.get('cat5', None)
        cat6 = request.POST.get('cat6', None)
        search = request.POST.get('category_ta', None)
        
        if search is not None and search != '':
            cat = Category.objects.get(name=search)
        elif cat6 is not None and cat6 != '__jcombo__':
            cat = Category.objects.get(id=cat6)
        elif cat5 is not None and cat5 != '__jcombo__':
            cat = Category.objects.get(id=cat5)
        elif cat4 is not None and cat4 != '__jcombo__':
            cat = Category.objects.get(id=cat4)
        elif cat3 is not None and cat3 != '__jcombo__':
            cat = Category.objects.get(id=cat3)
        elif cat2 is not None and cat2 != '__jcombo__':
            cat = Category.objects.get(id=cat2)
        else:
            cat = Category.objects.get(id=cat1)
            
        p.categories.add(cat)
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
    
    if 'image_button' in request.POST:
        imageuploadform = ImageUploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid:
            status = uploadimage(request, p.pk, imageuploadform)
            return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))
            
    return render_to_response('parts/detail.html', 
                              {'part': p, 
                               'metadata_form': metaform, 
                               'xref_form' : xrefform,
                               'imageuploadform' : imageuploadform,
                               'buylinkform' : buylinkform,
                               'mlt': mlt,
                               'page_title': title,
                               'agg_pricing': pricing,
                               'ditributor_skus': distributor_skus,
                               'asinform': asinform,
                              },
                              context_instance=RequestContext(request))

@login_required
def addmeta(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    metaform = MetadataForm(request.POST)
    if metaform.is_valid():
        key = metaform.cleaned_data['key'].strip().upper()
        value = metaform.cleaned_data['value'].strip().upper()
        attr = Attribute(key=key, value=value, user=request.user, part=p)
        try:
            attr.save()
            return True, attr.pk
        except IntegrityError:
            return 'Attribute already exists'

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
def addpart(request, part_number, company, desc):
    try:
        c = Company.objects.get(slug=slugify(company))
    except ObjectDoesNotExist:
        c = Company(name=company, slug=slugify(company))
        c.save()
    if Part.objects.filter(number=part_number, company=c).exists():
        newpart = Part.objects.get(number=part_number, company=c)
    else: 
        newpart = Part(number=part_number, company=c, user=request.user, description=desc, hits=0)
        newpart.save()
    return newpart

@login_required
def addpartform(request):
    if request.method == 'POST':
        partform = XrefForm(request.POST)
        if partform.is_valid():
            part_number = partform.cleaned_data['part'].upper()
            desc = partform.cleaned_data['desc'].upper()
            company = partform.cleaned_data['company'].upper()
            newpart = addpart(request, part_number, company, desc)
            return HttpResponseRedirect(newpart.get_absolute_url())
    else:
        partform = XrefForm()
    return render_to_response('parts/add.html',
                              {'partform': partform,},
                              context_instance=RequestContext(request))

@login_required
def addxref(request, part_id):
    p = get_object_or_404(Part, pk=part_id)
    xrefform = XrefForm(request.POST)
    if xrefform.is_valid():
        part_number = xrefform.cleaned_data['part'].strip().upper()
        company = xrefform.cleaned_data['company'].strip().upper()
        description = xrefform.cleaned_data['desc'].strip().upper()
        copy_attrs = xrefform.cleaned_data['copy_attrs']
        update_all_xrefs = xrefform.cleaned_data['update_all_xrefs']
        
        """Check if the company exists and create it if it does not"""
        try:
            c = Company.objects.get(slug=slugify(company))
        except ObjectDoesNotExist:
            c = Company(name=company, slug=slugify(company))
            c.save() 
        
        """Check if the cross referenced part exists and create it if it does not"""
        newpart, _created = Part.objects.get_or_create(number=part_number, company=c)
        if _created == True:
            newpart.user = request.user
            newpart.description = description
            newpart.hits = 0
            if copy_attrs == True:
                attributes = Attribute.objects.filter(part=part_id)
                for a in attributes:
                    new_attr = Attribute(key=a.key, value=a.value, part=newpart, upvotes=0, downvotes=0, user=request.user)
                    new_attr.save()
            newpart.save()

        newpart.cross_references.add(p)
        p.cross_references.add(newpart)

        if update_all_xrefs == True:
            for x in p.cross_references.all():
                x.cross_references.add(newpart)

        return True
            
@login_required
def uploadimage(request, part_id, form):
    print 'in uploadimage()'
    p = get_object_or_404(Part, pk=part_id)
    if form.is_valid():
        print 'form valid'
        if request.FILES.get('file', None):
            f = request.FILES['file']
            
            """ hash the image so we can keep them unique """
            #content = ContentFile(f.read()).read()
            #h = hashlib.sha512()
            #h.update(content)
            
            """Handle the file upload"""
            print 'changing file name'
            new_filename = "%s_%s" % (str(part_id), f.name)
            image = PartImage(user=request.user)
            try:
                print 'uploading image to aws'
                image.image.save(new_filename, f)
                image.save()
                p.images.add(image)
                p.save()
                print 'done'
                return True
            except IntegrityError:
                return False

            
    



