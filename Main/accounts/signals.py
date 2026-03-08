from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ManagerProfile, AssociateProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'manager':
            ManagerProfile.objects.create(user=instance)

        elif instance.role == 'associate':
            AssociateProfile.objects.create(user=instance)