from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import ExerciseService
from education.education_apps.educa.selectors import ExerciseSelectors


class ExerciseDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        answer = serializers.CharField()
        rank = serializers.IntegerField()

    def get(self, request, exercise_id):
        exercise = ExerciseSelectors().get_exercise(exercise_id)
        if exercise is None:
            raise Http404

        data = self.OutputSerializer(exercise).data
        return Response(data)

class ExerciseUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=False)
        answer = serializers.CharField(required=False)
        rank = serializers.IntegerField(required=False)

    def post(self, request, exercise_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exercise= ExerciseSelectors().get_exercise(exercise_id)
        if exercise is None:
            raise Http404
        exercise = ExerciseService().exercise_update(exercise=exercise, data=serializer.validated_data)

        data = ExerciseDetailApi.OutputSerializer(exercise).data
        return Response(data)

class ExerciseListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        rank = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        answer = serializers.CharField()
        rank = serializers.IntegerField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        exercises = ExerciseSelectors().exercise_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=exercises,
            request=request,
            view=self,
        )

class ExerciseCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=True)
        answer = serializers.CharField(required=True)
        rank = serializers.IntegerField(required=True)


    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exercise = ExerciseService().exercise_create(
            **serializer.validated_data
        )

        data = ExerciseDetailApi.OutputSerializer(exercise).data

        return Response(data)