from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import ControlTaskResultService
from education.education_apps.educa.selectors import ControlTaskResultSelectors, ExerciseSelectors


class ControlTaskResultDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        roster = serializers.CharField()
        control_task = serializers.CharField()
        answers = serializers.JSONField()#StringRelatedField(many=True)
        #exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        score = serializers.FloatField()
        created_at = serializers.DateField()
        check_in = serializers.BooleanField()


    def get(self, request, control_task_result_id):
        control_task_result = ControlTaskResultSelectors().get_control_task_result(control_task_result_id)
        if control_task_result is None:
            raise Http404
        data = self.OutputSerializer(control_task_result).data
        return Response(data)


class ControlTaskResultCheckInApi(APIView):

    class InputSerializer(serializers.Serializer):
        check_in = serializers.BooleanField()

    def post(self, request, control_task_result_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['check_in']:
            control_task_result = ControlTaskResultSelectors().get_control_task_result(control_task_result_id)
            if control_task_result is None:
                raise Http404
            control_task_result = ControlTaskResultService().control_task_result_update(
                control_task_result=control_task_result, data=serializer.validated_data
            )
            data = ControlTaskResultDetailApi.OutputSerializer(control_task_result).data
            return Response(data)
        raise Http404
class ControlTaskResultUpdateApi(APIView):
    pass
    # class InputSerializer(serializers.Serializer):
    #     description = serializers.CharField(required=False)
    #     questions = serializers.MultipleChoiceField(
    #         choices=[(q.id, q.id) for q in QuestionSelectors().question_list()])
    #     faculty_course = serializers.IntegerField()
    #
    # def post(self, request, control_test_id):
    #     serializer = self.InputSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     control_test = ControlTestSelectors().get_control_test(control_test_id)
    #     if control_test is None:
    #         raise Http404
    #     control_test = ControlTestService().control_test_update(control_test=control_test,
    #                                                             data=serializer.validated_data)
    #
    #     data = ControlTestDetailApi.OutputSerializer(control_test).data
    #     return Response(data)

class ControlTaskResultListApi(APIView):
    pass

    # class Pagination(LimitOffsetPagination):
    #      default_limit = 2
    #
    # class FilterSerializer(serializers.Serializer):
    #     id = serializers.IntegerField(required=False)
    #     roster = serializers.IntegerField(required=False)
    #     control_test = serializers.IntegerField(required=False)
    #     score = serializers.FloatField(required=False)
    #     check_in = serializers.BooleanField(required=False)
    #
    # class OutputSerializer(serializers.Serializer):
    #     id = serializers.IntegerField()
    #     roster = serializers.CharField()
    #     control_test = serializers.CharField()
    #     answers = serializers.JSONField()  # StringRelatedField(many=True)
    #     # exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #     score = serializers.FloatField()
    #     created_at = serializers.DateField()
    #     check_in = serializers.BooleanField()
    #     done_at = serializers.BooleanField()
    #
    # def get(self, request):
    #
    #     filters_sericlizer = self.FilterSerializer(data=request.query_params)
    #     filters_sericlizer.is_valid(raise_exception=True)
    #
    #     control_test_results = ControlTestResultSelectors().control_test_result_list()
    #     return get_pagination_response(
    #         pagination_class=self.Pagination,
    #         serializer_class=self.OutputSerializer,
    #         queryset=control_test_results,
    #         request=request,
    #         view=self,
    #     )

class ControlTaskResultCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        roster = serializers.IntegerField()
        control_task = serializers.IntegerField()
        answers_lst = serializers.ListField()
    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_task_result = ControlTaskResultService().control_task_result_create(
            **serializer.validated_data,
        )

        data = ControlTaskResultDetailApi.OutputSerializer(control_task_result).data

        return Response(data)

