from django.shortcuts import render

# Create your views here.

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Activity
from .serializers import ActivitySerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_feed(request):
    cache_key = f"feed_{request.user.id}"
    feed = cache.get(cache_key)

    if not feed:
        feed = Activity.objects.filter(user__in=request.user.following.all())[:50]
        cache.set(cache_key, feed, timeout=300)

    serializer = ActivitySerializer(feed, many=True)
    return Response(serializer.data)
