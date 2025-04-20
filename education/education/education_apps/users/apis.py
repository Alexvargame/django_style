from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)
from education.education_apps.users.models import BaseUser
from education.education_apps.users.selectors import user_get, user_list
from education.education_apps.users.services import user_create, user_update

from education.education_apps.educa.services import StudentService#student_create


class UserDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        email = serializers.CharField()

    def get(self, request, user_id):
        user = user_get(user_id)
        if user is None:
            raise Http404

        data = self.OutputSerializer(user).data
        return Response(data)

class UserListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.BooleanField(required=False, allow_null=True, default=None)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ('id', 'email', 'is_admin','is_student')
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )

class UserCreateApi(APIView):
    class Inputserializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.Inputserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(
            **serializer.validated_data
        )
        data = UserDetailApi.OutputSerializer(user).data
        return Response(data)

class UserBecomeStudentApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        surname = serializers.CharField(required=True)
        faculty = serializers.CharField(required=True)
        is_student = serializers.BooleanField(default=False)

    def post(self, request, user_id):


        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_get(user_id)
        if user.name != '':
            serializer.validated_data['name'] = user.name
        if user.surname != '':
            serializer.validated_data['surname'] = user.surname

        user.is_student = serializer.validated_data['is_student']
        user.name = serializer.validated_data['name']
        user.surname = serializer.validated_data['surname']
        del serializer.validated_data['is_student']
        user.save()
        if user.is_student:
            student = StudentService.student_create(
                **serializer.validated_data, user=user
            )
        user.student = student
        if user is None:
            raise Http404
        data = UserDetailApi.OutputSerializer(user).data
        return Response(data)

class UserUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        surname = serializers.CharField(required=True)

    def post(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_get(user_id)
        user.name = serializer.validated_data['name']
        user.surname = serializer.validated_data['surname']
        user.save()
        if user is None:
            raise Http404
        data = UserDetailApi.OutputSerializer(user).data
        return Response(data)












