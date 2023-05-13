from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import ProfileSerializer
from .models import Profile
from django.shortcuts import get_object_or_404

# Create your views here.




class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)


    def profile_details(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = User.objects.get(user=self.request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def update(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = User.objects.filter(user=self.request.user)
        userprofile = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(userprofile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)