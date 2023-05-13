from rest_framework import serializers
from .models import Category, Question, Answer, Chat

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class DocumentationChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"