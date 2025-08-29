from rest_framework import serializers
from .models import Question, Answer
import logging


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'user_id', 'text']

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source='answer_set')
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        logging.info(f"Создан новый вопрос: {question}")
        return question