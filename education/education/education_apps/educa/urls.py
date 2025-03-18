from django.urls import path
from .apis.student_apis import StudentUpdateApi, StudentDetailApi, StudentListApi
from .apis.faculty_apis import FacultyDetailApi, FacultyUpdateApi, FacultyListApi, FacultyCreateApi
from .apis.faculty_courses_apis import FacultyCourseCreateApi, FacultyCourseDetailApi, FacultyCourseListApi, FacultyCourseUpdateApi
from .apis.roster_apis import RosterCreateApi, RosterDetailApi, RosterListApi, RosterDeactivatedAtApi
from .apis.question_apis import QuestionCreateApi, QuestionUpdateApi, QuestionDetailApi, QuestionListApi
from .apis.exercise_apis import ExerciseCreateApi, ExerciseUpdateApi, ExerciseDetailApi, ExerciseListApi
from .apis.control_task_apis import ControlTaskDetailApi, ControlTaskCreateApi, ControlTaskListApi, ControlTaskUpdateApi
from .apis.control_test_apis import ControlTestListApi, ControlTestCreateApi, ControlTestDetailApi, ControlTestUpdateApi

urlpatterns = [
    path('students/', StudentListApi.as_view(), name='students_list'),
    path('students/<int:student_id>/', StudentDetailApi.as_view(), name='student_detail'),
    path('students/<int:student_id>/update/', StudentUpdateApi.as_view(), name='student_update'),

    path('facultys/<int:faculty_id>/', FacultyDetailApi.as_view(), name='faculty_name'),
    path('facultys/', FacultyListApi.as_view(), name='faculty_list'),
    path('facultys/<int:faculty_id>/update/', FacultyUpdateApi.as_view(), name='faculty_update'),
    path('facultys/create/', FacultyCreateApi.as_view(), name='faculty_create'),

    path('faculty_courses/create/', FacultyCourseCreateApi.as_view(), name='faculty_course_create'),
    path('faculty_courses/<int:faculty_course_id>/', FacultyCourseDetailApi.as_view(),
         name='faculty_course_detail'),
    path('faculty_courses/', FacultyCourseListApi.as_view(), name='faculty_courses_list'),
    path('faculty_courses/<int:faculty_course_id>/update/', FacultyCourseUpdateApi.as_view(),
         name='faculty_course_update'),

    path('rosters/create/', RosterCreateApi.as_view(), name='rosert_create'),
    path('rosters/<int:roster_id>/', RosterDetailApi.as_view(), name='roster_detail'),
    path('rosters/', RosterListApi.as_view(), name='roster_list'),
    path('rosters/<int:roster_id>/deactivated/', RosterDeactivatedAtApi.as_view(), name = 'roster_deactivated'),

    path('questions/create/', QuestionCreateApi.as_view(), name='question_create'),
    path('questions/<int:question_id>/update/', QuestionUpdateApi.as_view(), name='question_update'),
    path('questions/<int:question_id>/', QuestionDetailApi.as_view(), name='question_detail'),
    path('questions/', QuestionListApi.as_view(), name='question_list'),

    path('exercises/create/', ExerciseCreateApi.as_view(), name='exercise_create'),
    path('exercises/<int:exercise_id>/update/', ExerciseUpdateApi.as_view(), name='exercise_update'),
    path('exercises/<int:exercise_id>/', ExerciseDetailApi.as_view(), name='exercise_detail'),
    path('exercises/', ExerciseListApi.as_view(), name='exercise_list'),

    path('control_tasks/create/', ControlTaskCreateApi.as_view(), name='control_task_create'),
    path('control_tasks/', ControlTaskListApi.as_view(), name='control_task_list'),
    path('control_tasks/<int:control_task_id>/', ControlTaskDetailApi.as_view(), name='control_task_detail'),
    path('control_tasks/<int:control_task_id>/update/', ControlTaskUpdateApi.as_view(), name='control_task_update'),

    path('control_tests/create/', ControlTestCreateApi.as_view(), name='control_test_create'),
    path('control_tests/', ControlTestListApi.as_view(), name='control_test_list'),
    path('control_tests/<int:control_test_id>/', ControlTestDetailApi.as_view(), name='control_test_detail'),
    path('control_tests/<int:control_test_id>/update/', ControlTestUpdateApi.as_view(), name='control_test_update'),

]