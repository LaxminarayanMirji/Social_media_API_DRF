from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils.timezone import now


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=16)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def _str_(self):
        return f"{self.username} | {self.email}"


class Post(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=150)
    image = models.ImageField(blank=True, null=True,
                              upload_to="user_content_images")
    video = models.FileField(blank=True, null=True,
                             upload_to="user_content_videos",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def _str_(self):
        return self.title


class PostLike(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("post", "user"))


class PostComment(models.Model):
    comment_text = models.CharField(max_length=264)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)


class UserFollow(models.Model):
    user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name="src_follow")
    follows = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name="dest_follow")

class Activity(models.Model):
    ACTION_TYPES = [
        ('post_created', 'Post Created'),
        ('liked', 'Liked'),
        ('commented', 'Commented'),
        ('followed', 'Followed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    target_user = models.ForeignKey(User, related_name="target_user", on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} {self.get_action_type_display()} {self.post or self.target_user}"
