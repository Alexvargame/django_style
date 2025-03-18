from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import FacultyService
from education.education_apps.educa.selectors import FacultySelectors


class FacultyDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.SlugField()

    def get(self, request, faculty_id):
        faculty = FacultySelectors().get_faculty_by_id(faculty_id)
        if faculty is None:
            raise Http404

        data = self.OutputSerializer(faculty).data
        return Response(data)

class FacultyUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
    def post(self, request, faculty_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        faculty = FacultySelectors().get_faculty_by_id(faculty_id)
        if faculty is None:
            raise Http404
        faculty = FacultyService().faculty_update(fauclty=faculty, data=serializer.validated_data)
        data = FacultyDetailApi.OutputSerializer(faculty).data
        return Response(data)

class FacultyListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        slug = serializers.SlugField()
    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        facultys = FacultySelectors().faculty_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=facultys,
            request=request,
            view=self,
        )

class FacultyCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)


    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        faculty = FacultyService().faculty_create(
            **serializer.validated_data
        )
        data = FacultyDetailApi.OutputSerializer(faculty).data

        return Response(data)