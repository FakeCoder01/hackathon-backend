from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import DepartmentSerializer, PositionSerializer, OfficeSerializer
from .models import Department, Position, Office

from django.shortcuts import get_object_or_404

# Create your views here.




class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_departments(self):
        queryset = Department.objects.all()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Department.objects.filter(id=id) :
            department = Department.objects.get(id=id)
            serializer = self.get_serializer(department, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "No department"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)


class PositionViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_positions(self, department_id):
        queryset = Position.objects.filter(department_id=department_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Position.objects.filter(id=id) :
            position = Position.objects.get(id=id)
            serializer = self.get_serializer(position, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "No position"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)
    
class OfficeViewSet(viewsets.ModelViewSet):
    serializer_class = OfficeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_offices(self):
        queryset = Office.objects.all()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Office.objects.filter(id=id) :
            office = Office.objects.get(id=id)
            serializer = self.get_serializer(office, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "no office"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)

