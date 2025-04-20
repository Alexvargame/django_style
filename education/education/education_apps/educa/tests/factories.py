from datetime import timedelta

import factory
from django.utils.text import slugify

from education.education_apps.educa.models import (
    Roster,
    Faculty,
    FacultyCourse,
    Student,
)
from education.education_apps.educa.utils.tests.base import faker

class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Faculty

    name = factory.LazyAttribute(lambda _: f"{faker.unique.company()} Faculty" )
    slug = factory.LazyAttribute(lambda  self: slugify(self.name))

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student


    #user = factory.LazyAttribute(lambda _:faker.unique.user())
    identifier = factory.LazyAttribute(lambda _: faker.unique.uuid4())
    faculty = factory.SubFactory(FacultyFactory)

class FacultyWithStudentsFactory(FacultyFactory):
    @factory.post_generation
    def students(obj, create, extracted, **kwargs):
        if create:
            students = extracted or StudentFactory.create_batch(kwargs.pop('count', 5), **kwargs)
            obj.students.set(students)
            return students

class FacultyCourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FacultyCourse

    name = factory.LazyAttribute(lambda _: faker.unique.sentence(nb_words=3)[:-1])
    slug = factory.LazyAttribute(lambda self: slugify(self.name))
    faculty = factory.SubFactory((FacultyFactory))
    start_date = factory.LazyAttribute(lambda _: faker.past_date())
    end_date = factory.LazyAttribute(lambda self: self.start_date + timedelta(days=365))

class RosterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Roster

    student = factory.SubFactory(StudentFactory)
    faculty_course = factory.SubFactory(
        FacultyCourseFactory, faculty = factory.LazyAttribute(lambda course: course.factory_parent_student.faculty)

    )
    start_date = factory.LazyAttribute(lambda _self: _self.faculty_course.start_date)
    end_date = factory.LazyAttribute(lambda _self: _self.faculty_course.end_date)

def get_future_roster_start_date(roster_obj):
    if not roster_obj.start_after:
        return faker.future_date()
    return roster_obj.start_after + timedelta(days=faker.pyint(2, 100))

class FutureRosterFactory(RosterFactory):
    class Params:
        start_after = None
    start_date = factory.LazyAttribute(get_future_roster_start_date)

class FacultyCourseRosterFactory(FacultyCourseFactory):
    @factory.post_generation
    def roster(obj, create, extrated, **kwargs):
        if create:
            rosters = extracted or RosterFactory.create_batch(
                kwargs.pop("count", 5), **kwargs, student__faculty=obj.faculty  # NOTE!
            )

            obj.rosters.set(rosters)

            return rosters





















