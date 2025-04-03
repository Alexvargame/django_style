from typing import List, Optional

from django.db import transaction

from education.education_apps.common.services import model_update
from education.education_apps.users.models import BaseUser

@transaction.atomic
def user_create(*, email, is_active=True, is_admin=False, is_superuser=False, is_student=False, password=None):
    print("AARGD", email, is_active, is_admin, is_superuser, is_student, password)
    user = BaseUser.objects.create_user(email=email, is_active=is_active, is_admin=is_admin,
                                        is_superuser=is_superuser, is_student=is_student, password=password)

    return user

@transaction.atomic
def user_update(*,user, data):
    non_side_effect_fields =[]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)
    return user













