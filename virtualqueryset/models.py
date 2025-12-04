"""Base models for virtual models."""

from django.db import models


class VirtualModel(models.Model):
    """Base class for virtual models (no database table).

    Virtual models behave like Django models but don't have database tables.
    They use in-memory QuerySets to display data from external sources.

    Features:
    - No migrations created
    - No database queries
    - Compatible with Django admin
    - Read-only by default

    Example:
        class ConfigSetting(VirtualModel):
            key = models.CharField(max_length=255)
            value = models.TextField()
            
            objects = ConfigQuerySetManager('MY_SETTINGS')
            
            def __str__(self):
                return self.key
    """

    class Meta:
        abstract = True
        managed = False

    def save(self, *args, **kwargs):
        """Prevent saving virtual models.

        Override in subclass if you want to implement custom save logic
        (e.g., saving to API, file, cache).
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} is a virtual model and cannot be saved to database. "
            "Override save() if you want to implement custom persistence."
        )

    def delete(self, *args, **kwargs):
        """Prevent deleting virtual models.

        Override in subclass if you want to implement custom delete logic.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} is a virtual model and cannot be deleted from database. "
            "Override delete() if you want to implement custom deletion."
        )


class ReadOnlyVirtualModel(VirtualModel):
    """Virtual model that is explicitly read-only.

    Similar to VirtualModel but with more descriptive error messages.
    """

    class Meta:
        abstract = True
        managed = False

    def save(self, *args, **kwargs):
        """Read-only models cannot be saved."""
        raise NotImplementedError(
            f"{self.__class__.__name__} is read-only and cannot be modified."
        )

    def delete(self, *args, **kwargs):
        """Read-only models cannot be deleted."""
        raise NotImplementedError(
            f"{self.__class__.__name__} is read-only and cannot be deleted."
        )
