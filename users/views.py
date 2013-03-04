from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

from users.models import UserProfile, UserFavoritePart
from reputation.models import ReputationAction
from parts.models import Part

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    profile.profile_views += 1
    profile.save()
    reputation_actions = ReputationAction.objects.filter(user=user)

    return render_to_response('users/profile.html',
                              {'profile' : profile,
                               'reputation_actions' : reputation_actions,
                              },
                              context_instance=RequestContext(request))
                              
@login_required
def view_favorites(request):
    fave_parts = UserFavoritePart.objects.filter(user=request.user)
    user_parts = Part.objects.filter(user=request.user)
    
    return render_to_response('users/favorites.html',
                              {'fave_parts': fave_parts,
                               'user_parts': user_parts,
                              },
                              context_instance=RequestContext(request))
                              
@login_required
def edit_favorite_notes(request):
    f_pk = request.POST.get('fave-id', '')
    notes = request.POST.get('notes', '')
    fave_parts = UserFavoritePart.objects.filter(user=request.user)
    user_parts = Part.objects.filter(user=request.user)
    f = get_object_or_404(UserFavoritePart, pk=f_pk)
    if f.user == request.user:
        f.notes = notes
        f.save()
        if request.is_ajax:
            return render_to_response('users/includes/faveparts-table.html',
                                      {'fave_parts': fave_parts,
                                       'user_parts': user_parts,
                                      },
                                      context_instance=RequestContext(request))
        else:
            pass
    else:
        return HttpResponseBadRequest
                
                              
@login_required
def index(request):
    users = UserProfile.objects.all().order_by('user__username')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    p = Paginator(users, 10, request=request)
    try:
        results_list = p.page(page)
    except (PageNotAnInteger, EmptyPage):
        results_list = p.page(1)
    
    return render_to_response('users/index.html',
                              {'userlist': results_list,
                               'page_num': page,
                              },
                              context_instance=RequestContext(request))


