from django import template
from authentication.models import Profile, User

register = template.Library()

@register.simple_tag
def get_profile_image(user_id):
    try:
        user = User.objects.get(id=user_id)
        profile= Profile.objects.get(user=user) 
        return profile.image.url 
    except Profile.DoesNotExist:
        return 'assets/images/Sample_User.jpeg'