# Generated by Django 5.1.7 on 2025-06-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePageUser', '0004_remove_notification_family_task_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='accepted',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
