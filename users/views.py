from users.models import UserProfile, UserFavoritePart
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()

    return render_to_response('users/profile.html',
                              {'user_profile' : profile,
                              },
                              context_instance=RequestContext(request))
                              
@login_required
def view_favorites(request):
    fave_parts = UserFavoritePart.objects.filter(user=request.user)
    
    return render_to_response('users/favorites.html',
                              {'fave_parts': fave_parts,
                              },
                              context_instance=RequestContext(request))
                              
@login_required
def index(request):
    users = UserFavoritePart.objects.filter(user=request.user)
    
    return render_to_response('users/index.html',
                              {'userlist': users,
                              },
                              context_instance=RequestContext(request))


