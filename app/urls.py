from django.urls import path
from app.views import user, post
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/create/', user.CreateUserGV.as_view(), name='create-user'),
    path('user/login/', user.LoginUserAPIView.as_view(), name='login'),
    path('user/<int:pk>/', user.RetrieveUserAPIView.as_view(), name='profile'),
    path('user/update/', user.UpdateUserAPIView.as_view(), name='update-profile'),
    path('user/delete/<int:pk>/',
         user.DestroyUserAPIView.as_view(), name='delete-profile'),

    path('posts/', post.RetrieveUserPostsGV.as_view(), name='all-post'),
    path('post/create/', post.CreatePostGV.as_view(), name='create-post'),
    path('post/<int:pk>/', post.RetrievePostGV.as_view(), name='selected-post'),
    path('post/update/<int:pk>/', post.UpdatePostGV.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', post.DestroyPostGV.as_view(), name='delete-post'),

    path('post/like/<int:pk>/', post.LikePostAPIView.as_view(), name='like-post'),

    path('post/comment/<int:pk>/',
         post.CommentPostGV.as_view(), name='comment-post'),

    path('user/follow/<int:pk>/', post.FollowUserAPIView.as_view(),
         name='follow/unfollow-post'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
