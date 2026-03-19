from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from Users.models import Level, Types


@receiver(post_save, sender=User)
def run_on_superuser_create(sender, instance, **kwargs):
    Level.objects.update_or_create(user=instance)
    Types.objects.update_or_create(user=instance)