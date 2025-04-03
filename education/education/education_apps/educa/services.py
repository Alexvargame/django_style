from django.db import transaction
from django.utils.text import slugify
from collections import OrderedDict
from django.core.exceptions import ValidationError

from education.education_apps.educa.models import (Student, Faculty, FacultyCourse, Roster, Question,
                                                   Exercise, ControlTest, ControlTask, ControlTestResult,
                                                   ControlTaskResult)
from education.education_apps.common.services import model_update
from education.education_apps.educa.static_data import slovar

from education.education_apps.educa.selectors import (ControlTaskSelectors, ExerciseSelectors,
                                                      QuestionSelectors, ControlTestResultSelectors,
                                                      RosterSelectors, ControlTestSelectors,
                                                        )
ROSTER_CREATE_DIFFERENT_FACULTYS = (
    "Cannot roster {student} in {faculty_course}"
)
ROSTER_VALIDATE_PERIOD_OUTSIDE_COURSE_PERIOD = 'Roster period cannot be outside {faculty_course} period'
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

    def roster_faculty_course_validate(self, student, faculty_course):
        print(student, faculty_course)
        print(type(student), type(faculty_course))
        print(student.faculty_id, faculty_course.faculty_id)
        if student.faculty_id != faculty_course.faculty_id:
            raise ValidationError(
                ROSTER_CREATE_DIFFERENT_FACULTYS.format(
                    student=student.__str__(),
                    faculty_course=faculty_course.__str__()# или faculty_course.__str__()
                )
            )
        else:
            print('NO ERROR RAISED')

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
        # expected_message = f"Cannot roster {student.identifier} in {faculty_course.name}"
        #
        #
        # with self.assertRaisesMessage(ValidationError, expected_message):
        # self.roster_faculty_course_validate(student, course)
        self.roster_faculty_course_validate(student, faculty_course)
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
        control_test.average_rank = round(control_test.average_rank)
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

class ControlTestResultService:

    def value_dict(self):
        return {'answer': '', 'right_answer': ''}
    @transaction.atomic
    def control_test_result_create(self, roster, control_test, answers_lst):
        roster = RosterSelectors().get_roster(roster_id=roster)
        control_test = ControlTestSelectors().get_control_test(control_test_id=control_test)
        control_test_result = ControlTestResult.objects.create(roster=roster, control_test=control_test)
        answers = OrderedDict.fromkeys([ct.id for ct in control_test.questions.all()],self.value_dict())
        for i in range(len(answers_lst)):
            answers[list(answers.keys())[i]]['answer'] = answers_lst[i]
        control_test_result.answers = answers
        control_test_result.save()
        return control_test_result

    @transaction.atomic
    def control_test_result_update(self, control_test_result, data):
        non_side_effect_fields = ['check_in']
        control_test_result, has_updated = model_update(instance=control_test_result, fields=non_side_effect_fields, data=data)
        for ans in control_test_result.control_test.questions.all():
            control_test_result.answers[str(ans.id)]['right_answer'] = ans.answer
            if (control_test_result.answers[str(ans.id)]['answer'] == ans.answer
                    or control_test_result.answers[str(ans.id)]['answer'] == ans.choice_answer[ans.answer]) :
                control_test_result.score += ans.rank
        control_test_result.save()
        return control_test_result

class ControlTaskResultService:

    def value_dict(self):
        return {'answer': '', 'right_answer': ''}
    @transaction.atomic
    def control_task_result_create(self, roster, control_task, answers_lst):
        roster = RosterSelectors().get_roster(roster_id=roster)
        control_task = ControlTaskSelectors().get_control_task(control_task_id=control_task)
        control_task_result = ControlTaskResult.objects.create(roster=roster, control_task=control_task)
        answers = OrderedDict.fromkeys([ct.id for ct in control_task.exercises.all()],self.value_dict())
        for i in range(len(answers_lst)):
            answers[list(answers.keys())[i]]['answer'] = answers_lst[i]
        control_task_result.answers = answers
        control_task_result.save()
        return control_task_result

    @transaction.atomic
    def control_task_result_update(self, control_task_result, data):
        non_side_effect_fields = ['check_in']
        control_task_result, has_updated = model_update(instance=control_task_result,
                                                        fields=non_side_effect_fields, data=data)
        for ans in control_task_result.control_task.exercises.all():
            control_task_result.answers[str(ans.id)]['right_answer'] = ans.answer
            if control_task_result.answers[str(ans.id)]['answer'] == ans.answer:
                control_task_result.score += ans.rank
        control_task_result.save()
        return control_task_result