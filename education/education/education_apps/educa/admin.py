from django.contrib import admin

from .models import (Student, Faculty, FacultyCourse, Roster, Question, Exercise,
                     ControlTask, ControlTest, ControlTestResult, ControlTaskResult)

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
    readonly_fields = ('average_rank', )

    def save_model(self, *args, **kwargs):
        print(self.model, self.model.average_rank.field)
        print(self.model.exercises.field)
        print(dir(self.model.average_rank.field))
        self.model.average_rank.field.value = 1
        super().save_model(*args, **kwargs)
@admin.register(ControlTest)
class ControlTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'faculty_course','description', 'get_questions', 'average_rank')

@admin.register(ControlTestResult)
class ControlTestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'roster','control_test', 'answers', 'score', 'check_in', 'created_at')

@admin.register(ControlTaskResult)
class ControlTaskResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'roster','control_task', 'answers', 'score', 'check_in', 'created_at')