from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import FacultyCourseService
from education.education_apps.educa.selectors import FacultyCourseSelectors, FacultySelectors


class FacultyCourseDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.SlugField()
        faculty = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def get(self, request, faculty_course_id):
        faculty_course = FacultyCourseSelectors().get_faculty_course_by_id(faculty_course_id)
        if faculty_course is None:
            raise Http404

        data = self.OutputSerializer(faculty_course).data
        return Response(data)

class FacultyCourseUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        faculty = serializers.CharField(required=False)
        start_date = serializers.CharField(required=False)
        end_date = serializers.CharField(required=False)

    def post(self, request, faculty_course_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['faculty'] = FacultySelectors().get_faculty_by_name(
            serializer.validated_data['faculty'])
        faculty_course = FacultyCourseSelectors().get_faculty_course_by_id(faculty_course_id)
        if faculty_course is None:
            raise Http404
        faculty_course = FacultyCourseService().faculty_update(faculty_course=faculty_course, data=serializer.validated_data)
        data = FacultyCourseDetailApi.OutputSerializer(faculty_course).data
        return Response(data)

class FacultyCourseListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        start_date = serializers.CharField(required=False)
        end_date = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.SlugField()
        faculty = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        faculty_courses = FacultyCourseSelectors().faculty_courses_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=faculty_courses,
            request=request,
            view=self,
        )

class FacultyCourseCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        faculty = serializers.CharField(required=True)
        start_date = serializers.CharField(required=True)
        end_date = serializers.CharField(required=True)


    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        faculty = FacultySelectors().get_faculty_by_name(serializer.validated_data['faculty'])
        del serializer.validated_data['faculty']
        print('DEL', serializer.validated_data)

        if faculty is None:
            raise Http404
        faculty_course = FacultyCourseService().faculty_course_create(
            **serializer.validated_data, faculty=faculty,
        )

        data = FacultyCourseDetailApi.OutputSerializer(faculty_course).data

        return Response(data)