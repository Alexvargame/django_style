from typing import Optional

from django.db.models.query import QuerySet

from education.education_apps.common.utils import get_object
from education.education_apps.educa.filters import (StudentFilters, FacultyFilters,
                                                    FacultyCourseFilters, RosterFilters,
                                                    QuestionFilters, ExerciseFilters,
                                                    ControlTaskFilters, ControlTestFilters
                                                    )
from education.education_apps.educa.models import (Student, Faculty,
                                                   FacultyCourse, Roster, Question, Exercise,
                                                   ControlTest, ControlTask
                                                   )

class StudentSelectors:

    def get_student(self, student_id):
        student = get_object(Student, id=student_id)
        return student

    def get_student_by_identifier(self, student_ident):
        student = get_object(Student, identifier=student_ident)
        return student

    def student_list(self, filters=None):
        filters = filters or {}
        qs = Student.objects.all()
        return StudentFilters(filters, qs).qs


class FacultySelectors:

    def get_faculty_by_name(self, faculty_name):
        return get_object(Faculty, name=faculty_name)

    def get_faculty_by_id(self, faculty_id):
        return get_object(Faculty, id=faculty_id)

    def faculty_list(self, filters=None):
        filters = filters or {}
        qs = Faculty.objects.all()
        return FacultyFilters(filters, qs).qs

class FacultyCourseSelectors:

    def get_faculty_course_by_name(self, faculty_course_name, faculty):
        return get_object(FacultyCourse, name=faculty_course_name, faculty=faculty)

    def get_faculty_course_by_id(self, faculty_course_id):
        return get_object(FacultyCourse, id=faculty_course_id)

    def faculty_courses_list(self, filters=None):
        filters = filters or {}
        qs = FacultyCourse.objects.all()
        return FacultyCourseFilters(filters, qs).qs

class RosterSelectors:

    def get_roster(self, roster_id):
        roster = Roster.objects.get(id=roster_id)
        return roster

    def roster_list(self, filters=None):
        filters = filters or {}
        qs = Roster.objects.all()
        return RosterFilters(filters, qs).qs

class QuestionSelectors:

    def get_question(self, question_id):
        question = Question.objects.get(id=question_id)
        return question
    def question_list(self, filters=None):
        filters = filters or {}
        qs = Question.objects.all()
        return QuestionFilters(filters, qs).qs

class ExerciseSelectors:

    def get_exercise(self, exercise_id):
        exercise = Exercise.objects.get(id=exercise_id)
        return exercise
    def exercise_list(self, filters=None):
        filters = filters or {}
        qs = Exercise.objects.all()
        return ExerciseFilters(filters, qs).qs

class ControlTaskSelectors:

    def get_control_task(self, control_task_id):
        control_task = ControlTask.objects.get(id=control_task_id)
        return control_task
    def control_task_list(self, filters=None):
        filters = filters or {}
        qs = ControlTask.objects.all()
        return ControlTaskFilters(filters, qs).qs

class ControlTestSelectors:

    def get_control_test(self, control_test_id):
        control_test = ControlTest.objects.get(id=control_test_id)
        return control_test
    def control_test_list(self, filters=None):
        filters = filters or {}
        qs = ControlTest.objects.all()
        return ControlTestFilters(filters, qs).qs
