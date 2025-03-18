from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import ControlTestService
from education.education_apps.educa.selectors import ControlTestSelectors,QuestionSelectors


class ControlTestDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        questions = serializers.StringRelatedField(many=True)
        #exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        average_rank = serializers.FloatField()
        faculty_course = serializers.CharField()

    def get(self, request, control_test_id):
        control_test = ControlTestSelectors().get_control_test(control_test_id)
        if control_test is None:
            raise Http404
        data = self.OutputSerializer(control_test).data
        return Response(data)

class ControlTestUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=False)
        questions = serializers.MultipleChoiceField(
            choices=[(q.id, q.id) for q in QuestionSelectors().question_list()])
        faculty_course = serializers.IntegerField()

    def post(self, request, control_test_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_test = ControlTestSelectors().get_control_test(control_test_id)
        if control_test is None:
            raise Http404
        control_test = ControlTestService().control_test_update(control_test=control_test,
                                                                data=serializer.validated_data)

        data = ControlTestDetailApi.OutputSerializer(control_test).data
        return Response(data)

class ControlTestListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        average_rank = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        questions = serializers.StringRelatedField(many=True)
        average_rank = serializers.IntegerField()
        faculty_course = serializers.CharField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        control_tests = ControlTestSelectors().control_test_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=control_tests,
            request=request,
            view=self,
        )

class ControlTestCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField()
        questions = serializers.MultipleChoiceField(choices=[(q.id, q.id) for q in QuestionSelectors().question_list()])
        faculty_course = serializers.IntegerField()

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_test = ControlTestService().control_test_create(
            **serializer.validated_data,
        )

        data = ControlTestDetailApi.OutputSerializer(control_test).data

        return Response(data)

