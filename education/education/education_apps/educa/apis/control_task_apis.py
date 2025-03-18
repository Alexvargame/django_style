from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import ControlTaskService
from education.education_apps.educa.selectors import ControlTaskSelectors, ExerciseSelectors


class ControlTaskDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        exercises = serializers.StringRelatedField(many=True)
        #exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        average_rank = serializers.FloatField()
        faculty_course = serializers.CharField()

    def get(self, request, control_task_id):
        control_task = ControlTaskSelectors().get_control_task(control_task_id)

        print('cOOOOOOOOOOOOOOO',control_task.exercises.all())
        if control_task is None:
            raise Http404
        data = self.OutputSerializer(control_task).data
        return Response(data)

class ControlTaskUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        description = serializers.CharField(required=False)
        exercises = serializers.MultipleChoiceField(
            choices=[(ex.id, ex.id) for ex in ExerciseSelectors().exercise_list()])
        faculty_course = serializers.IntegerField()

    def post(self, request, control_task_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_task = ControlTaskSelectors().get_control_task(control_task_id)
        if control_task is None:
            raise Http404
        control_task = ControlTaskService().control_task_update(control_task=control_task, data=serializer.validated_data)

        data = ControlTaskDetailApi.OutputSerializer(control_task).data
        return Response(data)

class ControlTaskListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        average_rank = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description = serializers.CharField()
        exercises = serializers.StringRelatedField(many=True)
        average_rank = serializers.IntegerField()
        faculty_course = serializers.CharField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        control_tasks = ControlTaskSelectors().control_task_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=control_tasks,
            request=request,
            view=self,
        )

class ControlTaskCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        description = serializers.CharField()
        exercises = serializers.MultipleChoiceField(choices=[(ex.id, ex.id) for ex in
                                                             ExerciseSelectors().exercise_list()])
        faculty_course = serializers.IntegerField()


    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        control_task = ControlTaskService().control_task_create(
            **serializer.validated_data,
        )

        data = ControlTaskDetailApi.OutputSerializer(control_task).data

        return Response(data)

#
# class VotingCreateSerializer(serializers.ModelSerializer):
#     vote_list = serializers.MultipleChoiceField(choices=[(p.id, p.name) for p in Pokemon.objects.all()],
#                                                 style={'base_template': 'select_multiple.html'})
#
#     class Meta:
#         model = Voting
#         fields = ('vote_name', 'vote_list', 'vote_result')
#
#     def create(self, validated_data):
#         voting = Voting.objects.update_or_create(
#             vote_name=validated_data.get('vote_name', None),
#             vote_result=validated_data.get('vote_result', None),
#         )
#
#         return voting
