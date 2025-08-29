import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Question, Answer


# Create your tests here.
@pytest.mark.django_db
class TestQuestion(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.question = Question.objects.create(text="Тестовое создание вопроса")
        self.answer = Answer.objects.create(
            question_id=self.question,
            user_id='qwerty_user_123',
            text="Тест Ответ на тестовый вопрос"
        )

    def test_get_all_questions(self):
        #Тест получения всех вопросов
        response = self.client.get('/api/v1/questions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_get_question_by_id(self):
        # Тест получения конкретного вопроса
        response = self.client.get(f'/api/v1/questions/{self.question.id}/')
        print(f"Response data type: {type(response.data)}")  # Отладка
        print(f"Response data: {response.data}")  # Отладка
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == "Тестовое создание вопроса"
        assert 'answers' in response.data

