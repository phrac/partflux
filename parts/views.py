from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify, truncatechars
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.sites.models import get_current_site
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage
from haystack.query import SearchQuerySet

from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from parts.models import Part, Xref, PartImage, BuyLink, Attribute
from companies.models import Company
from partgroups.models import PartGroup
from parts.forms import MetadataForm, XrefForm, ImageUploadForm, BuyLinkForm
from users.models import UserProfile, UserFavoritePart
import json

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
    
def detail(request, part_id, company_slug, part_slug):
    p = get_object_or_404(Part, id=part_id)
    mlt = SearchQuerySet().more_like_this(p)[:10]
    current_site = get_current_site(request)
    title = "%s by %s - %s | %s" % (p.number, p.company.name,
                                    truncatechars(p.description,
                                    (settings.MAX_PAGE_TITLE_LENGTH
                                     - (len(p.number) +
                                     len(p.company.name)
                                     + 22))),
                                    current_site.name)

    if request.user.is_authenticated() and UserFavoritePart.objects.filter(user=request.user, part=p).count() == 1:
        fave = UserFavoritePart.objects.get(user=request.user, part=p)
        is_user_favorite = True
    else:
        is_user_favorite = False
        fave = None
    
    if request.user.is_authenticated():
        user_asm = PartGroup.objects.filter(user=request.user)
    else:
        user_asm = None
    
    xrefs = Xref.objects.filter(part=p.id).exclude(xrefpart=p.id)
    reverse_xrefs = Xref.objects.filter(xrefpart=p.id).exclude(part=p.id)

    metaform = MetadataForm(None)
    xrefform = XrefForm(None)
    imageuploadform = ImageUploadForm(None)
    buylinkform = BuyLinkForm(None)

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

            if status is True:
                messages.success(request, 'Image upload successful. Thanks for contributing!')
            else:
                messages.error(request, 'Image upload failed. Most likely it was not an image file or it was a duplicate.')

            return HttpResponseRedirect(reverse('parts.views.detail',
                                                    args=[part_id, p.company.slug, p.slug]))
            
    return render_to_response('parts/detail.html', 
                              {'part': p, 
                               'xrefs': xrefs,
                               'reverse_xrefs': reverse_xrefs,
                               'metadata_form': metaform, 
                               'xref_form' : xrefform,
                               'imageuploadform' : imageuploadform,
                               'buylinkform' : buylinkform,
                               'is_user_favorite' : is_user_favorite,
                               'fave': fave,
                               'user_assemblies': user_asm,
                               'mlt': mlt,
                               'page_title': title,
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
    print 'adding xref' 
    if xrefform.is_valid():
        part_number = xrefform.cleaned_data['part'].strip().upper()
        company = xrefform.cleaned_data['company'].strip().upper()
        description = xrefform.cleaned_data['desc'].strip().upper()
        copy_attrs = xrefform.cleaned_data['copy_attrs']
        
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

        xr1, _created = Xref.objects.get_or_create(part=p, xrefpart=newpart)
        if _created == True:
            xr1.user = request.user
            xr1.save()
            return True
        else:
            return 'Cross Reference already exists'
            
@login_required
def uploadimage(request, part_id, form):
    import hashlib
    from django.core.files.base import ContentFile
    
    p = get_object_or_404(Part, pk=part_id)
    if form.is_valid():
        if request.FILES.get('file', None):
            f = request.FILES['file']
            
            """ hash the image so we can keep them unique """
            content = ContentFile(f.read()).read()
            h = hashlib.sha512()
            h.update(content)
            
            """Handle the file upload"""
            new_filename = "%s_%s" % (str(part_id), f.name)
            f.seek(0)
            image = PartImage(user=request.user, hash=h.hexdigest())
            try:
                image.image.save(new_filename, f)
                image.save()
                p.images.add(image)
                p.save()
                return True
            except IntegrityError:
                return False

            
    



