from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project
from accounts.models import ManagerProfile, AssociateProfile


@receiver(post_save, sender=Project)
def auto_assign_associates(sender, instance, **kwargs):

    if instance.manager:
        try:
            manager_profile = ManagerProfile.objects.get(
                user=instance.manager
            )

            associate_profiles = AssociateProfile.objects.filter(
                manager=manager_profile
            )

            associate_users = [a.user for a in associate_profiles]

            # Clear old and set new
            instance.associates.set(associate_users)

        except ManagerProfile.DoesNotExist:
            pass