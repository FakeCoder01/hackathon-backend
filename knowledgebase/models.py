from django.db import models
import uuid
from api.models import Profile
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    question = models.TextField()
    category = models.ForeignKey(Category, related_name="questions", on_delete=models.CASCADE)
    asked_by = models.ForeignKey(Profile, related_name="q_ask", on_delete=models.CASCADE)
    solved = models.BooleanField(default=False)
    tags = models.TextField(null=True, blank=True)
    def __str__(self) -> str:
        return self.question

class Answer(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.TextField()
    answerd_by = models.ForeignKey(Profile, related_name="q_ans", on_delete=models.CASCADE)
    helpful = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.question.question
    

class ChatHistory(models.Model):
    user = models.ForeignKey(Profile, related_name="chathistory_user_profile", on_delete=models.CASCADE)
    question = models.TextField(null=True, blank=True)
    chat_history = models.TextField(null=True, blank=True)

    