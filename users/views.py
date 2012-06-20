from users.models import UserProfile
from django.contrib.auth import User
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)

    return render_to_response('users/profile.html',
                              {'user_profile' : profile,
                              },
                              context_instance=RequestContext(request))


