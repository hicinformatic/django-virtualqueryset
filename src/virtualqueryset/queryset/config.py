"""ConfigQuerySet for Django settings as virtual models."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from django.conf import settings

from .base import InMemoryQuerySet


class ConfigQuerySet(InMemoryQuerySet):
    """QuerySet for Django configuration settings.

    Displays Django settings (INSTALLED_APPS, MIDDLEWARE, etc.) as virtual models
    in Django admin without database persistence.

    Example:
        class InstalledApp(models.Model):
            name = models.CharField(max_length=255)
            
            objects = ConfigQuerySetManager('INSTALLED_APPS')
            
            class Meta:
                managed = False
    """

    def __init__(
        self,
        model=None,
        data: Optional[List[Any]] = None,
        setting_name: Optional[str] = None,
        query=None,
        using=None,
        hints=None,
    ):
        """Initialize with Django setting name.

        Args:
            model: Django model class
            data: List of data (if already loaded)
            setting_name: Name of Django setting to load (e.g., 'INSTALLED_APPS')
            query: Django Query object
            using: Database alias (unused)
            hints: Query hints (unused)
        """
        if data is None and setting_name:
            data = self._load_from_setting(setting_name)

        super().__init__(
            model=model, data=data, query=query, using=using, hints=hints
        )
        self.setting_name = setting_name

    def _load_from_setting(self, setting_name: str) -> List[Any]:
        """Load data from Django setting.

        Args:
            setting_name: Name of the setting

        Returns:
            List of values from the setting
        """
        value = getattr(settings, setting_name, None)

        if value is None:
            return []

        if isinstance(value, (list, tuple)):
            return list(value)

        if isinstance(value, dict):
            return [{"key": k, "value": v} for k, v in value.items()]

        return [value]

    def reload(self):
        """Reload data from Django settings."""
        if self.setting_name:
            data = self._load_from_setting(self.setting_name)
            return self.__class__(
                self.model,
                data,
                self.setting_name,
                self.query.clone(),
                using=self._db,
                hints=self._hints,
            )
        return self._clone()

