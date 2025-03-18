from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError


from education.education_apps.api.pagination import (
    LimitOffsetPagination,
    get_pagination_response,
)


from education.education_apps.educa.services import RosterService
from education.education_apps.educa.selectors import FacultyCourseSelectors, StudentSelectors, RosterSelectors

ROSTER_CREATE_DIFFERENT_FACULTYS = "Cannot roster {surname} {name}  {identifier} in {faculty_course}"

class RosterCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        student = serializers.CharField(required=True)
        faculty_course = serializers.CharField(required=True)
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student = StudentSelectors().get_student_by_identifier(
            serializer.validated_data['student']
        )

        faculty_course = FacultyCourseSelectors().get_faculty_course_by_name(
            serializer.validated_data['faculty_course'], student.faculty
        )
        if faculty_course and faculty_course.faculty == student.faculty:
            roster = RosterService().roster_create(student, faculty_course,
                                                    serializer.validated_data['start_date'],
                                                    serializer.validated_data['end_date']
                                               )
        else:
            raise ValidationError(ROSTER_CREATE_DIFFERENT_FACULTYS.format(surname=student.surname, name=student.name, identifier=student.identifier,
                                                                          faculty_course=serializer.validated_data['faculty_course']))
        data = RosterDetailApi.OutputSerializer(roster).data
        return Response(data)

class RosterDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        student = serializers.CharField()
        faculty_course = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        active = serializers.BooleanField()
        deactivated_at = serializers.DateField()
    def get(self, request, roster_id):
        roster = RosterSelectors().get_roster(roster_id)
        if roster is None:
            raise Http404
        data = self.OutputSerializer(roster).data
        return Response(data)

class RosterDeactivatedAtApi(APIView):

    class InputSerializer(serializers.Serializer):
        deactivated_at = serializers.CharField(required=True)

    def post(self, request, roster_id):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roster = RosterSelectors().get_roster(roster_id)
        serializer.validated_data['active'] = False
        #serializer.validated_data['faculty'] = FacultySelectors().get_faculty_by_name(serializer.validated_data['faculty'])
        #serializer.validated_data['faculty'] = Faculty.objects.get(name=serializer.validated_data['faculty'])
        # roster.active = False/
        # roster.deactivated_at =
        print(serializer.validated_data)
        roster = RosterService().roster_deactivated_at(roster=roster,
                data=serializer.validated_data)
        data = RosterDetailApi.OutputSerializer(roster).data
        return Response(data)

class RosterListApi(APIView):

    class Pagination(LimitOffsetPagination):
         default_limit = 2

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        student = serializers.CharField(required=False)
        faculty_course = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        student = serializers.CharField(required=False)
        faculty_course = serializers.CharField(required=False)
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)
        active = serializers.BooleanField(required=False)
        deactivated_at = serializers.DateField(required=False)



    def get(self, request):

        filters_sericlizer = self.FilterSerializer(data=request.query_params)
        filters_sericlizer.is_valid(raise_exception=True)

        rosters = RosterSelectors().roster_list()
        return get_pagination_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=rosters,
            request=request,
            view=self,
        )