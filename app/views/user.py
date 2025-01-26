from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import User
from app.serializer import UserSerializer, UserLoginSerializer


class CreateUserGV(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


class LoginUserAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, __ = Token.objects.get_or_create(user=user)
            return Response({"success": True, "token": token.key},status=status.HTTP_200_OK)
        return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

class RetrieveUserAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

class RetrieveUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data,    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "user updated"},
                status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "error updating user","errors": serializer.errors}
            ,status=status.HTTP_400_BAD_REQUEST)

class DestroyUserAPIView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def destroy(self, request, pk):
        user = get_object_or_404(User, id=pk)
        if pk == request.user.id:
            self.perform_destroy(user)
            return Response({ "success": True, "message": "user deleted" },
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "success": False, "message": "not enough permissions" },
                            status=status.HTTP_403_FORBIDDEN)
