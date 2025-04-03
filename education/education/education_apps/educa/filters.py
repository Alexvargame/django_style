import django_filters

from django_filters import BaseInFilter, NumberFilter

from education.education_apps.educa.models import (Student, Faculty, Roster, FacultyCourse,
                                                   Question, Exercise, ControlTest, ControlTask,
                                                   ControlTaskResult, ControlTestResult)

class StudentFilters(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ('id', 'surname', 'identifier', 'faculty')

class FacultyFilters(django_filters.FilterSet):
    class Meta:
        model = Faculty
        fields = ('id', 'name')

class FacultyCourseFilters(django_filters.FilterSet):
    class Meta:
        model = FacultyCourse
        fields = ('id', 'start_date', 'end_date')

class RosterFilters(django_filters.FilterSet):
    class Meta:
        model = Roster
        fields = ('id', 'student', 'faculty_course')

class QuestionFilters(django_filters.FilterSet):
    id = NumberFilter()  # Для фильтрации по одному id
    id__in = BaseInFilter(field_name='id', lookup_expr='in')  # Для фильтрации по списку id
    class Meta:
        model = Question
        fields = ('id', 'rank')

class ExerciseFilters(django_filters.FilterSet):
    id = NumberFilter()  # Для фильтрации по одному id
    id__in = BaseInFilter(field_name='id', lookup_expr='in')  # Для фильтрации по списку id
    class Meta:
        model = Exercise
        fields = ('id', 'rank')

class ControlTaskFilters(django_filters.FilterSet):
    # id = NumberFilter()  # Для фильтрации по одному id
    # id__in = BaseInFilter(field_name='id', lookup_expr='in')  # Для фильтрации по списку id

    class Meta:
        model = ControlTask
        fields = ('id','average_rank')

class ControlTestFilters(django_filters.FilterSet):
    # id = NumberFilter()  # Для фильтрации по одному id
    # id__in = BaseInFilter(field_name='id', lookup_expr='in')  # Для фильтрации по списку id

    class Meta:
        model = ControlTest
        fields = ('id','average_rank')

class ControlTestResaltFilters(django_filters.FilterSet):
    score__gte = NumberFilter(field_name='score', lookup_expr='gte')  # Фильтр "больше или равно"
    score__lte = NumberFilter(field_name='score', lookup_expr='lte')  # Фильтр "меньше или равно"
    class Meta:
        model = ControlTestResult
        fields = ('id','roster', 'control_test', 'score', 'check_in')

class ControlTaskResaltFilters(django_filters.FilterSet):
    score__gte = NumberFilter(field_name='score', lookup_expr='gte')  # Фильтр "больше или равно"
    score__lte = NumberFilter(field_name='score', lookup_expr='lte')  # Фильтр "меньше или равно"
    class Meta:
        model = ControlTaskResult
        fields = ('id','roster', 'control_task', 'score', 'check_in')
#
# class ControlTaskFilters(django_filters.FilterSet):
#     id = NumberFilter()
#     id__in = BaseInFilter(field_name='id', lookup_expr='in')
#     average_rank__gte = NumberFilter(field_name='average_rank', lookup_expr='gte')  # Фильтр "больше или равно"
#     average_rank__lte = NumberFilter(field_name='average_rank', lookup_expr='lte')  # Фильтр "меньше или равно"
