from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SimpleModel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

class RandomModel(BaseModel):

    start_date = models.DateField()
    end_date = models.DateField()

    simple_ojects = models.ManyToManyField(SimpleModel, blank=True, related_name='random_objects')

    class Meta:
        constraints =[
            models.CheckConstraint(
                name='start_date_before_end_date', check=Q(start_date__lt=F('end_date'))
            )

        ]










