from django.shortcuts import get_object_or_404

from ..models import UserProfile
from ..forms import UserProfileForm


def handle_user_follow_or_unfollow_form(user_action, user_id, member_id):
    user_profile = get_object_or_404(
        UserProfile, pk=user_id)
    member_profile = get_object_or_404(
        UserProfile, pk=member_id)

    if user_action == 'follow':
        user_profile.following.add(member_profile)
    elif user_action == 'unfollow':
        user_profile.following.remove(member_profile)

def handle_user_profile_form(request, user, context):
    form = UserProfileForm(request, instance=user.profile)
    
    if form.is_valid():
        form.save()
        context.update({
            'user_profile_form': UserProfileForm(instance=user.profile),
        })