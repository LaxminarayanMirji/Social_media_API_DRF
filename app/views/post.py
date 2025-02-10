from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Post, PostComment, PostLike, User, UserFollow, Activity
from app.serializer import (PostSerializer, PostLikeSerializer,
                            CommentSerializer, UserFollowSerializer,
                            ActivitySerializer)
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes


class CreatePostGV(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RetrievePostGV(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UpdatePostGV(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"success": True, "message": "updated post"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "error updating post"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class DestroyPostGV(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            post = Post.objects.get(id=pk)
            if post.user.id == request.user.id:
                self.perform_destroy(post)
                return Response({"success": True, "message": "post deleted"},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"success": False, "message": "not enough permissions"},
                                status=status.HTTP_403_FORBIDDEN)
        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class RetrieveUserPostsGV(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_posts = Post.objects.filter(user=request.user.id)
        serializer = self.serializer_class(user_posts, many=True)
        return Response({"success": True, "posts": serializer.data},
                        status=status.HTTP_200_OK)


class LikePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            likes_list = PostLike.objects.filter(post=post)
            serializer = PostLikeSerializer(likes_list,
                                            many=True)
            return Response({"success": True, "likes_list": serializer.data},
                            status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            new_post_like, created = PostLike.objects.get_or_create(
                user=request.user, post=post)

            if not created:
                new_post_like.delete()
                return Response({"success": True, "message": "post unliked"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": True, "message": "post liked"},
                                status=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class CommentPostGV(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            comments = PostComment.objects.filter(post=post)
            serializer = self.serializer_class(comments, many=True)
            return Response({"success": True, "comments":  serializer.data},
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(post=post, user=request.user)
                return Response({"success": True, "message": "comment added"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "message": "error adding a comment"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"success": False, "message": "post does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class FollowUserAPIView(APIView):
    queryset = UserFollow.objects.all()
    serializer_class = UserFollowSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        following = UserFollow.objects.filter(user=request.user)
        followers = UserFollow.objects.filter(follows=request.user)
        following_serializer = UserFollowSerializer(
            following, many=True)
        followers_serializer = UserFollowSerializer(
            followers, many=True)
        return Response({"success": True, "following": following_serializer.data,
                         "followers": followers_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            following_user = User.objects.get(id=pk)
            follow_user, created = UserFollow.objects.get_or_create(
                user=request.user, follows=following_user)
            if not created:
                follow_user.delete()
                return Response({"success": True, "message": "unfollowed user"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"success": True, "message": "followed user"},
                                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"success": False, "message": "following user does not exist"},
                            status=status.HTTP_404_NOT_FOUND)



class ActivityFeedGV(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        cache_key = f"feed_{self.request.user.id}"
        feed = cache.get(cache_key)

        if not feed:
            feed = Activity.objects.filter(user__in=self.request.user.following.all())[:50]
            cache.set(cache_key, feed, timeout=300)

        return feed