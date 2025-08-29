from rest_framework.response import Response
from rest_framework.views import APIView
from tt_app.serializers import QuestionSerializer, AnswerSerializer, QuestionCreateSerializer
from tt_app.models import Question, Answer
from rest_framework import status

import logging
logger = logging.getLogger('tt_app')

# Create your views here.
class QuestionAPIviews(APIView):
    def get(self, request, id=None):
        try:
            if id:
                #GET /questions/{id} — получить вопрос и все ответы на него
                logger.info(f"Получение вопроса с id={id}")
                question = Question.objects.get(id=id)
                return Response(QuestionSerializer(question).data)
            # GET /questions/ — список всех вопросов
            logger.info("Запрос списка всех вопросов")
            all_questions = Question.objects.all()
            return Response(QuestionSerializer(all_questions, many=True).data)
        except Exception as e:
            logger.error(f"Ошибка при получении ответа от questions: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)

    def post(self, request):
        #POST /questions — создать новый вопрос
        try:
            logger.info(f"Создание нового вопроса: {request.data}")
            serializer = QuestionCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # вызовет create() метод сериализатора
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при создании вопроса questions: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)

    def delete(self, request, id=None):
        # DELETE /questions/{id} — удалить вопрос (вместе с ответами)
        try:
            if id:
                try:
                    question = Question.objects.get(id=id)
                    question.delete()
                    logger.info(f"Вопрос с id={id} удален успешно")
                    return Response({'message': 'Question deleted successfully'}, status=200)
                except Question.DoesNotExist:
                    logger.warning(f"Попытка удаления несуществующего вопроса id={id}")
                    return Response({'error': 'Question does not exist'}, status=404)
            logger.warning("Попытка удаления без указания id")
            return Response({'error': 'Question does not exist'}, status=404)

        except Exception as e:
            logger.error(f"Ошибка при удалении вопроса: {str(e)}")
            return Response({'error': 'Internal server error'}, status=500)


class AnswerAPIviews(APIView):
    def get(self, request, id=None):
        #GET /answers/{id} — получить конкретный ответ
        if id:
            answer = Answer.objects.get(id=id)
            return Response(QuestionSerializer(answer, many=False).data)
        return Response({'error': 'Answer does not exist'}, status=404)

    def post(self, request, id=None):
        #POST /questions/{id}/answers/ — добавить ответ к вопросу
        data = request.data
        data.update({"question_id": id})
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        #DELETE /answers/{id} — удалить ответ
        if id:
            answer = Answer.objects.get(id=id)
            answer.delete()
            return Response({'message': 'Answer deleted successfully'}, status=200)
        return Response({'error': 'Answer does not exist'}, status=404)
