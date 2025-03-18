from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import StudentService
from education.education_apps.educa.selectors import StudentSelectors, FacultySelectors


class StudentDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        surname = serializers.CharField()
        faculty = serializers.CharField()
        #email = serializers.EmailField()
        identifier = serializers.CharField()
    def get(self, request, student_id):
        student = StudentSelectors().get_student(student_id)
        if student is None:
            raise Http404

        data = self.OutputSerializer(student).data
        return Response(data)

class StudentUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        faculty = serializers.CharField(required=True)

    def post(self, request, student_id):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = StudentSelectors().get_student(student_id)
        serializer.validated_data['faculty'] = FacultySelectors().get_faculty_by_name(serializer.validated_data['faculty'])
        #serializer.validated_data['faculty'] = Faculty.objects.get(name=serializer.validated_data['faculty'])
        student = StudentService().student_update(student=student,
                data=serializer.validated_data)
        data = StudentDetailApi.OutputSerializer(student).data
        return Response(data)

class StudentListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        surname = serializers.CharField(required=False)
        identifier = serializers.CharField(required=False)
        faculty = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        surname = serializers.CharField()
        faculty = serializers.CharField()
        #email = serializers.EmailField()
        identifier = serializers.CharField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        students = StudentSelectors().student_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=students,
            request=request,
            view=self,
        )