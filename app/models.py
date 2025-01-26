from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


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
