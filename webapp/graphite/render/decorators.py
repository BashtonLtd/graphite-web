from django.shortcuts import get_object_or_404
from django.http import Http404

from graphite.account.models import Profile


def check_target(view):
  def decorator(request, *args, **kwargs):
    user = request.user

    # Allow staff users to view any target
    if user.is_staff:
      return view(request, *args, **kwargs)

    target = request.GET['target']

    profile = get_object_or_404(Profile, user=user)
    user_targets = profile.targets.split(',')
    # Check each target set in profile against url target
    for user_target in user_targets:
      if target.startswith(user_target):
        return view(request, *args, **kwargs)

    raise Http404
  return decorator