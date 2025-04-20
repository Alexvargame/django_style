from datetime import timedelta
from unittest.mock import patch

import education.education_apps.educa.services
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from education.education_apps.educa.models import Roster
from education.education_apps.educa.apis.roster_apis import (
    ROSTER_CREATE_DIFFERENT_FACULTYS,
    RosterCreateApi
)
from education.education_apps.educa.services import RosterService

from education.education_apps.educa.tests.factories import (
    FacultyCourseFactory,
    StudentFactory
)

class RosterCreateTests(TestCase):
    def test_setvice_raises_error_if_different_faculty(self):
        print('TEST #11111111111111111111111111111111111111111')
        student = StudentFactory.create(name='AI')#build()
        faculty_course = FacultyCourseFactory.create()#.build()


        msg = ROSTER_CREATE_DIFFERENT_FACULTYS.format(surname=student.surname,
                                                                     name=student.name,
                                                                     identifier=student.identifier,
                                                                     faculty_course=faculty_course)
        with self.assertRaisesMessage(
            ValidationError, msg):
            RosterService().roster_create(student=student, faculty_course=faculty_course,
                                          start_date=faculty_course.start_date, end_date=faculty_course.end_date)
        self.assertEqual(Roster.objects.count(), 0)

    @patch('education.education_apps.educa.services.RosterService')#().roster_validate_period')
    def test_service_does_not_create_roster_if_period_is_not_valid(self, roster_validate_period_mock):
        roster_validate_period_mock.side_effect=ValidationError("")
        faculty_course = FacultyCourseFactory.create()#build()
        student = StudentFactory.create()#build()
        with self.assertRaises(ValidationError):
            RosterService().roster_create(student=student,
                                          faculty_course=faculty_course,
                                          start_date=faculty_course.start_date,
                                          end_date=faculty_course.end_date)
        self.assertEqual(Roster.objects.count(), 0)

    @patch('education.education_apps.educa.services.RosterService')#().roster_validate_period')
    def test_service_uses_faculty_period_for_default_period(self, roster_validate_period_mock):
        faculty_course = FacultyCourseFactory()
        student = StudentFactory(faculty=faculty_course.faculty)
        roster = RosterService().roster_create(student=student,
                                               faculty_course=faculty_course,
                                               start_date=faculty_course.start_date,
                                               end_date=faculty_course.end_date)
        self.assertEqual(roster.start_date, faculty_course.start_date)
        self.assertEqual(roster.end_date, faculty_course.end_date)

    @patch('education.education_apps.educa.services.RosterService')#().roster_validate_period')
    def test_service_doesn_not_school_course_period_if_dates_are_passed(self, roster_validate_period_mock):
        faculty_course = FacultyCourseFactory()
        student = StudentFactory(faculty=faculty_course.faculty)

        start_date = timezone.now().date()
        end_date = faculty_course.end_date - timedelta(days=1)

        roster = RosterService().roster_create(student=student, faculty_course=faculty_course,
                                               start_date=start_date, end_date=end_date)

        self.assertEqual(roster.start_date, start_date)
        self.assertEqual(roster.end_date, end_date)










