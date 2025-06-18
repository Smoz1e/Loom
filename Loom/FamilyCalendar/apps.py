from django.apps import AppConfig


class FamilycalendarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FamilyCalendar'

    def ready(self):
        import FamilyCalendar.models  # noqa
