from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'mehtod': 'DELETE'})


class UserProfileView(APIView):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.UpdateOwnProfile]

    def get(self, request, pk=None, format=None):
        """Get all profiles"""
        if pk:
            user = get_object_or_404(models.UserProfile.objects.all(), pk=pk)
            serializer = self.serializer_class(user)
            return Response({'user': serializer.data})
        else:
            users = models.UserProfile.objects.all()
            serializer = self.serializer_class(users, many=True)
            return Response({'users': serializer.data})

    def post(self, request):
        """Create new profile"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_saved = serializer.save()
            return Response({"Success": "User created succesfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """update existing profile"""
        user = get_object_or_404(models.UserProfile.objects.all(), pk=pk)
        serializer = self.serializer_class(instance=user,data=request.data)

        if serializer.is_valid():
            user_saved = serializer.save()
            return Response({"Success": "User updated succesfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """partial update existing profile"""
        user = get_object_or_404(models.UserProfile.objects.all(), pk=pk)
        serializer = self.serializer_class(instance=user,data=request.data, partial=True)

        if serializer.is_valid():
            user_saved = serializer.save()
            return Response({"Success": "User updated succesfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """delete existing profile"""
        user = get_object_or_404(models.UserProfile.objects.all(), pk=pk)
        user.delete()

        return Response({"Success": "User deleted succesfully"}, status=status.HTTP_200_OK)



class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retreive, update, partial_update',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message':'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retreive(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http method': 'DELETE'})
