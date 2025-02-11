
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Activity
from app.models import Post, PostLike, UserFollow

@receiver(post_save, sender=Post)
def create_post_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(user=instance.user, action_type='post_created', post=instance)

@receiver(post_save, sender=PostLike)
def create_like_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(user=instance.user, action_type='liked', post=instance.post)

@receiver(post_save, sender=UserFollow)
def create_follow_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(user=instance.user, action_type='followed', target_user=instance.follows)
