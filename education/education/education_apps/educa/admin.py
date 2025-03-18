from django.contrib import admin

from .models import (Student, Faculty, FacultyCourse, Roster, Question, Exercise,
                     ControlTask, ControlTest)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'surname', 'identifier', 'user', 'faculty')
    search_fields = ('email',)
    list_filter = ('faculty',)

@admin.register(FacultyCourse)
class FacultyCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'faculty', 'start_date', 'end_date')
    #prepopulated_fields = {'slug': ('name',)}
    search_fields = ('faculty', )
    list_filter = ('start_date', 'end_date')

@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'faculty_course', 'start_date', 'end_date', 'active', 'deactivated_at')
    list_filter = ('student', 'faculty_course')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'choice_answer', 'answer', 'rank')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'answer', 'rank')

@admin.register(ControlTask)
class ControlTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty_course', 'description', 'get_exercises', 'average_rank')


@admin.register(ControlTest)
class ControlTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty_course','description', 'get_questions', 'average_rank')
