from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import ImageSerializer, ExperienceSerializer, SocailSerializer
from .models import Image, Experience, Social


# Create your views here.




class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_images(self):
        queryset = Image.objects.filter(profile=self.request.user.userprofile)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Image.objects.filter(id=id) :
            image = Image.objects.get(id=id)
            serializer = self.get_serializer(image, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(profile=self.request.user.userprofile)
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "No Image"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=self.request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_experiences(self):
        queryset = Experience.objects.filter(profile=self.request.user.userprofile)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Experience.objects.filter(id=id) :
            experience = Experience.objects.get(id=id)
            serializer = self.get_serializer(experience, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(profile=self.request.user.userprofile)
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "No Experience"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)
    
class SocailViewSet(viewsets.ModelViewSet):
    serializer_class = SocailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_socails(self):
        queryset = Social.objects.filter(profile=self.request.user.userprofile)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Social.objects.filter(id=id) :
            socail = Social.objects.get(id=id)
            serializer = self.get_serializer(socail, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "no social"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=self.request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)

