# Generated by Django 5.0.7 on 2025-03-13 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('educa', '0009_remove_roster_unigue_roster_roster_unigue_roster'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roster',
            old_name='deactiveted_at',
            new_name='deactivated_at',
        ),
    ]
