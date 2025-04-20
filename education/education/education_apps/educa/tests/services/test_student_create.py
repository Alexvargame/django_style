from datetime import timedelta
from unittest.mock import patch

import education.education_apps.educa.services
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from education.education_apps.educa.models import Student
from education.education_apps.users.services import user_create
from education.education_apps.educa.services import StudentService
#from education.education_apps.educa.services import RosterService

from education.education_apps.educa.tests.factories import (
    FacultyCourseFactory,
    FacultyFactory
)
from education.education_apps.educa.utils.tests.base import faker



class StudentCreateTests(TestCase):
    #def test_student_is_rostered_to_all_active_school_courses(self):
    def test_student_create(self):
        print('TEST STUDENT CREATE')

        faculty = FacultyFactory()
        email = faker.unique.email()
        user = user_create(email=email, is_active=True, is_admin=False, is_superuser=False, is_student=False, password=None)
        print(user)
        student = StudentService().student_create(name=user.name, surname=user.surname, user=user,
                                                  faculty=faculty)
        self.assertEqual(student.user.email, email)
        self.assertEqual(student.faculty, faculty)