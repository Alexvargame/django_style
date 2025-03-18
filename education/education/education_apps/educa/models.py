from django.db import models
from django.db.models import Q, F
from uuid import uuid4
from education.education_apps.users.models import BaseUser

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.name

class Student(models.Model):

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    #email = models.EmailField()
    identifier = models.UUIDField(default=uuid4)
    faculty = models.ForeignKey(Faculty, related_name='faculty_students', on_delete=models.CASCADE)
    #user = models.ForeignKey(BaseUser, related_name='user_student', on_delete=models.CASCADE, unique=True)
    user = models.OneToOneField(BaseUser, related_name='user_student', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        # unique_together = (
        #     ("identifier", "faculty"),
        #     ("identifier", "user"),
        # )

    def __str__(self):
        return f'Студент {self.user}: {self.identifier}'

class FacultyCourse(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    faculty = models.ForeignKey(Faculty, related_name='faculty_courses', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        constraints =[
            models.CheckConstraint(
                name= 'faculty_course_start_before_end',
                check=Q(start_date__lt=F('end_date')),
            )
        ]
        unique_together = (
            (
                "name",
                "faculty",
                "start_date",
                "end_date",
            ),
        )

    def __str__(self):
        return f"{self.name} in {self.faculty}"

class Roster(models.Model):

    student = models.ForeignKey(Student, related_name='rosters', on_delete=models.CASCADE)
    faculty_course = models.ForeignKey(FacultyCourse, related_name='rosters', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    deactivated_at = models.DateField(null=True, blank=True)


    class Meta:
        verbose_name = 'Список'
        verbose_name_plural = 'Списки'
        constraints = [
            models.CheckConstraint(
                name="roster_start_before_end", check=Q(start_date__lt=F("end_date"))
            ),
            models.UniqueConstraint(
                fields=["student",
                "faculty_course",
                # "start_date",
                # "end_date"
                        ],
                name='unigue_roster'
            )
        ]
        # unique_together = (
        #     (
        #         "student",
        #         "faculty_course",
        #         "start_date",
        #         "end_date",
        #     ),
        # )

class Exercise(models.Model):

    description = models.CharField(max_length=1000)
    answer = models.CharField(max_length=100)
    rank = models.IntegerField()

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self):
        return self.description

class Question(models.Model):
    description = models.CharField(max_length=1000)
    choice_answer = models.JSONField()
    answer = models.CharField(max_length=100)
    rank = models.IntegerField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.description


class ControlTask(models.Model):
    description = models.CharField(max_length=100)
    exercises = models.ManyToManyField(Exercise, related_name='task_exercises')
    average_rank = models.FloatField(default=0.0)
    faculty_course = models.ForeignKey(FacultyCourse, related_name='control_tasks',
                                       on_delete=models.CASCADE, default=3)

    class Meta:
        verbose_name = 'Контрольная работа'
        verbose_name_plural = 'Контрольные работы'

    def __str__(self):
        return self.description

    def get_exercises(self):
        return [ex for ex in self.exercises.all()]

class ControlTest(models.Model):
    description = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, related_name='test_questions')
    average_rank = models.FloatField(default=0.0)
    faculty_course = models.ForeignKey(FacultyCourse, related_name='control_tests',
                                       on_delete=models.CASCADE, default=3)

    class Meta:
        verbose_name = 'Контрольный тест'
        verbose_name_plural = 'Контрольные тесты'

    def __str__(self):
        return self.description

    def get_questions(self):
        return [q for q in self.questions.all()]