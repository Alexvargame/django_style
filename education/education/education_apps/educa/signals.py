
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Exercise


@receiver(post_save, sender=Exercise)
@receiver(post_delete, sender=Exercise)
def update_control_task_average_rank(sender, instance, **kwargs):
    # Получаем все ControlTask, связанные с этим Exercise
    print('SSIIIIIIIIIIIIIIIIIIII')
    control_tasks = instance.task_exercises.all()
    for control_task in control_tasks:
        control_task.save()  # Вызов save пересчитает average_rank