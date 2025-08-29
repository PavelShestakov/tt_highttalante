from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=32, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}_{self.text}"

class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=256, default='')
    text = models.CharField(max_length=32, default='')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id}_{self.question_id}_{self.text}"









