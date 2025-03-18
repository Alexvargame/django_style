from typing import Optional

from django.db.models.query import QuerySet

from education.education_apps.common.utils import get_object
from education.education_apps.users.filters import BaseUserFilter
from education.education_apps.users.models import BaseUser

def user_get_login_data(*, user):
    return {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }
def user_list(*, filters=None):
    filters = filters or {}
    qs = BaseUser.objects.all()
    return BaseUserFilter(filters, qs).qs

def user_get(user_id):
    user = get_object(BaseUser, id=user_id)
    return user






























































