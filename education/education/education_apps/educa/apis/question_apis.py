from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import QuestionService
from education.education_apps.educa.selectors import QuestionSelectors


class QuestionDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        choice_answer = serializers.JSONField()
        answer = serializers.CharField()
        rank = serializers.IntegerField()


    def get(self, request, question_id):

        question = QuestionSelectors().get_question(question_id)
        if question is None:
            raise Http404

        data = self.OutputSerializer(question).data
        return Response(data)

class QuestionUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=False)
        choice_answer = serializers.JSONField(required=False)
        answer = serializers.CharField(required=False)
        rank = serializers.IntegerField(required=False)

    def post(self, request, question_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = QuestionSelectors().get_question(question_id)
        if question is None:
            raise Http404
        question = QuestionService().question_update(question=question, data=serializer.validated_data)

        data = FacultyCourseDetailApi.OutputSerializer(question).data
        return Response(data)

class QuestionListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        rank = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        choice_answer = serializers.JSONField()
        answer = serializers.CharField()
        rank = serializers.IntegerField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        questions = QuestionSelectors().question_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=questions,
            request=request,
            view=self,
        )

class QuestionCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=True)
        choice_answer = serializers.JSONField(required=True)
        answer = serializers.CharField(required=True)
        rank = serializers.IntegerField(required=True)


    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = QuestionService().question_create(
            **serializer.validated_data
        )

        data = FacultyCourseDetailApi.OutputSerializer(question).data

        return Response(data)