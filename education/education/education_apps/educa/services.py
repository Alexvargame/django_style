from django.db import transaction
from django.utils.text import slugify

from django.core.exceptions import ValidationError

from education.education_apps.educa.models import (Student, Faculty, FacultyCourse, Roster, Question,
                                                   Exercise, ControlTest, ControlTask)
from education.education_apps.common.services import model_update
from education.education_apps.educa.static_data import slovar

from education.education_apps.educa.selectors import ControlTaskSelectors, ExerciseSelectors, QuestionSelectors

ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD = "Roster period cannot be outside {faculty_course} period"
class StudentService:

    @transaction.atomic
    def student_create(self, *, name, surname, user, faculty):
        faculty = Faculty.objects.get(name=faculty)
        student = Student.objects.create(name=name, surname=surname, user=user, faculty=faculty)
        return student

    @transaction.atomic
    def student_update(self, student, data):
        non_side_effect_fields = ['faculty']
        student, has_updated = model_update(instance=student, fields=non_side_effect_fields, data=data)
        return student

class FacultyService:

    @transaction.atomic
    def faculty_update(self, faculty, data):
        non_side_effect_fields = ['name']
        faculty, has_updated = model_update(instance=faculty, fields=non_side_effect_fields, data=data)
        return faculty

    @transaction.atomic
    def faculty_create(self, name):
        slug = slugify(name,'ru')
        # slug = slug.translate(
        #     str.maketrans(
        #         "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        #         "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS:Y_EUA"
        # ))
        for key in slovar:
            slug = slug.replace(key, slovar[key])
        faculty = Faculty.objects.create(name=name, slug=slug)
        return faculty

class FacultyCourseService:

    @transaction.atomic
    def faculty_course_create(self, name, faculty, start_date, end_date):
        slug = slugify(name, 'ru')
        for key in slovar:
            slug = slug.replace(key, slovar[key])
        slug = faculty.slug + '_' + slug
        faculty_course = FacultyCourse.objects.create(name=name, slug=slug, faculty=faculty,
                                                      start_date=start_date, end_date=end_date)
        return faculty_course

    @transaction.atomic
    def faculty_update(self, faculty_course, data):
        non_side_effect_fields = ['name', 'faculty', 'start_date', 'end_date']
        faculty_course, has_updated = model_update(instance=faculty_course, fields=non_side_effect_fields, data=data)
        return faculty_course

class RosterService:

    def roster_validate_period(self, start_date, end_date, faculty_course):

        start_date_validation = start_date >= faculty_course.start_date and start_date < faculty_course.end_date
        end_date_validation = (
            end_date <= faculty_course.end_date and end_date > faculty_course.start_date and end_date > start_date
        )

        if not start_date_validation or not end_date_validation:
            raise (ValidationError(ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD.format(faculty_course=faculty_course)))

    @transaction.atomic
    def roster_create(self, student, faculty_course, start_date, end_date):
        start_date = start_date or faculty_course.start_date
        end_date = end_date or faculty_course.end_date
        self.roster_validate_period(start_date, end_date, faculty_course)
        roster = Roster.objects.create(
            student=student, faculty_course=faculty_course,
            start_date=start_date, end_date=end_date
        )
        return roster

    @transaction.atomic
    def roster_deactivated_at(self, roster, data):
        non_side_effect_fields = ['active', 'deactivated_at']
        faculty_course, has_updated = model_update(instance=roster, fields=non_side_effect_fields, data=data)
        return faculty_course

class QuestionService:

    @transaction.atomic
    def question_create(self, description, choice_answer, answer, rank):
        question = Question.objects.create(description=description, choice_answer=choice_answer,
                                   answer=answer, rank=rank)
        return question

    @transaction.atomic
    def question_update(self, question, data):
        non_side_effect_fields = ['description', 'choice_answer', 'answer', 'rank']
        question, has_updated = model_update(instance=question, fields=non_side_effect_fields, data=data)
        return question

class ExerciseService:

    @transaction.atomic
    def exercise_create(self, description, answer, rank):
        exercise = Exercise.objects.create(description=description,
                                   answer=answer, rank=rank)
        return exercise

    @transaction.atomic
    def exercise_update(self, exercise, data):
        non_side_effect_fields = ['description',  'answer', 'rank']
        exercise, has_updated = model_update(instance=exercise, fields=non_side_effect_fields, data=data)
        return exercise

class ControlTaskService:

    @transaction.atomic
    def control_task_create(self, description, exercises, faculty_course):
        choice_exercises = ExerciseSelectors().exercise_list(filters={'id__in': list(exercises)})
        average_rank = round(sum([ex.rank for ex in choice_exercises]) / len(choice_exercises), 2)
        control_task = ControlTask.objects.create(description=description, average_rank=average_rank,
                                                  faculty_course=FacultyCourse.objects.get(id=faculty_course))
        control_task.exercises.set(choice_exercises)
        control_task.save()
        return control_task

    @transaction.atomic
    def control_task_update(self, control_task, data):
        print(data)
        non_side_effect_fields = ['description', 'exercises', 'faculty_course']
        data['faculty_course'] = FacultyCourse.objects.get(id=data['faculty_course'])
        control_task, has_updated = model_update(instance=control_task, fields=non_side_effect_fields, data=data)
        average_rank = round(sum([ex.rank for ex in control_task.exercises.all()]) / len(control_task.exercises.all()), 2)
        control_task.average_rank = average_rank
        control_task.save()
        return control_task

class ControlTestService:

    @transaction.atomic
    def control_test_create(self, description, questions, faculty_course):
        choice_questions = QuestionSelectors().question_list(filters={'id__in': list(questions)})
        average_rank = round(sum([ex.rank for ex in choice_questions]) / len(choice_questions), 2)
        control_test = ControlTest.objects.create(description=description, average_rank=average_rank,
                                                  faculty_course=FacultyCourse.objects.get(id=faculty_course))
        control_test.questions.set(choice_questions)
        control_test.save()
        return control_test

    @transaction.atomic
    def control_test_update(self, control_test, data):
        non_side_effect_fields = ['description', 'questions', 'faculty_course']
        data['faculty_course'] = FacultyCourse.objects.get(id=data['faculty_course'])
        control_test, has_updated = model_update(instance=control_test, fields=non_side_effect_fields, data=data)
        average_rank = round(sum([ex.rank for ex in control_test.questions.all()]) / len(control_test.questions.all()), 2)
        control_test.average_rank = average_rank

        control_test.save()
        return control_test