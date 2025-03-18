import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from education.education_apps.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, is_superuser=False, is_student=False,
                    password=None):
        if not email:
            raise ValueError("Users musr have email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )
        user.is_superuser=True
        user.save(using=self._db)
        return user

class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    surname = models.CharField(max_length=100, blank=True, null=True, default='')
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    jwt_key = models.UUIDField(default=uuid.uuid4)
    is_student = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="baseuser_set",  # Уникальное имя для обратной связи
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="baseuser_set",  # Уникальное имя для обратной связи
        related_query_name="user",
    )
    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


# Create your models here.
