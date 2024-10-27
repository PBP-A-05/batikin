from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import logging

logger = logging.getLogger(__name__)

DEFAULT_PROFILE_PICTURE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOizmxkQV5rf4N9ayOC3pojndp0nzIDAFUtg&s"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    logger.info(f"Signal triggered for user {instance.username}, created: {created}")
    
    if created:
        logger.info(f"Creating new profile for user {instance.username}")
        profile = Profile.objects.create(
            user=instance,
            profile_picture=DEFAULT_PROFILE_PICTURE
        )
        logger.info(f"Profile created for {instance.username} with picture: {profile.profile_picture}")
    else:
        logger.info(f"Updating profile for existing user {instance.username}")
        profile, profile_created = Profile.objects.get_or_create(user=instance)
        if profile_created:
            logger.info(f"Profile was not found, created new one for {instance.username}")
        if not profile.profile_picture:
            profile.profile_picture = DEFAULT_PROFILE_PICTURE
            profile.save()
            logger.info(f"Updated profile picture for {instance.username} to default")
        else:
            logger.info(f"Profile picture for {instance.username} already set: {profile.profile_picture}")

    logger.info(f"Signal processing completed for {instance.username}")