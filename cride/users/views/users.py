"""Users views."""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cride.users.serializers import UserLoginSerializer, UserModelSerializer, UserSignupSerializer, AccountVerificationSerialzier

class UserLoginAPIView(APIView):
    """User login API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignupAPIView(APIView):
    """User signup API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    """Account verify API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = AccountVerificationSerialzier(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'OK'}
        return Response(data, status=status.HTTP_200_OK)