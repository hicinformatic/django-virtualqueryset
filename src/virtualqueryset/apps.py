"""Django app configuration."""

from django.apps import AppConfig


class VirtualQuerySetConfig(AppConfig):
    """Configuration for the virtualqueryset app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "virtualqueryset"
    verbose_name = "Virtual QuerySet"

