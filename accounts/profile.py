# accounts/profile.py
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from accounts.forms import UserProfileForm


# noinspection PyUnresolvedReferences
def retrieve(request):
    """ gets the UserProfile instance for a user, or creates one if it does not exist
        note that this requires an authenticated user before we try calling it
    """
    try:
        # profile = request.user.get_profile()
        profile = request.user.myprofile.user_profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user_profile=request.user)
        profile.save()
    return profile


def set_(request):
    """ updates the information stored in the user's profile """
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()



