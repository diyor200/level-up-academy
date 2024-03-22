from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

from .models import Homework

@receiver(post_save, sender=Homework)
def handle_new_instance(sender, instance, created, **kwargs):
    if created:
        print("New instance created:", instance)
    
