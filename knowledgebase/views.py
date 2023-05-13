from django.shortcuts import render
from .models import Category, Question, Answer
from .serializers import CategorySerializer, QuestionSerializer, AnswerSerializer

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def category_details(self):
        queryset = Category.objects.all()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def update(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = Category.objects.filter(id=id)
        category = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(category, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)


class QusetionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_questions(self):
        queryset = Question.objects.filter(profile=self.request.user.userprofile)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Question.objects.filter(id=id) :
            question = Question.objects.get(id=id)
            serializer = self.get_serializer(question, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(asked_by=self.request.user.userprofile)
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "no question"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(asked_by=self.request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)
    

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def all_answers(self, q_id):
        if not Question.objects.filter(id=q_id).exists():
            return Response({"detail" : "no answer"}, status=404)
        queryset = Answer.objects.filter(question=q_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

    def update(self, request, id):
        if Answer.objects.filter(id=id) :
            answer = Answer.objects.get(id=id)
            serializer = self.get_serializer(answer, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(answerd_by=self.request.user.userprofile)
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"detail" : "no question"}, status=400)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=self.request.user.userprofile)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=400)


