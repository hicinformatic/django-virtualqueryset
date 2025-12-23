"""Managers for virtual models."""

from typing import Any, Callable, List, Optional

from django.db import models

from .queryset.base import InMemoryQuerySet
from .queryset.config import ConfigQuerySet
from .queryset.api import APIQuerySet
from .queryset.json_qs import JSONQuerySet
from .queryset.cached import CachedQuerySet


class VirtualManager(models.Manager):
    """Base manager for virtual models (no database).

    Subclass and override get_data() to provide data source.

    Example:
        class MyVirtualModel(models.Model):
            name = models.CharField(max_length=255)
            
            objects = MyCustomManager()
            
            class Meta:
                managed = False
    """

    queryset_class = InMemoryQuerySet

    def get_queryset(self):
        """Return queryset with data from get_data()."""
        data = self.get_data()
        return self.queryset_class(model=self.model, data=data)

    def get_data(self) -> List[Any]:
        """Override this method to provide data source.

        Returns:
            List of model instances or dictionaries
        """
        return []


class ConfigQuerySetManager(VirtualManager):
    """Manager that loads data from Django settings.

    Args:
        setting_name: Name of Django setting to load
    """

    queryset_class = ConfigQuerySet

    def __init__(self, setting_name: str):
        """Initialize with setting name.

        Args:
            setting_name: Django setting name (e.g., 'INSTALLED_APPS')
        """
        super().__init__()
        self.setting_name = setting_name

    def get_queryset(self):
        """Return queryset with data from Django setting."""
        return self.queryset_class(
            model=self.model, setting_name=self.setting_name
        )


class APIQuerySetManager(VirtualManager):
    """Manager that loads data from external API.

    Args:
        fetch_func: Callable that fetches data from API
        cache_timeout: Cache duration in seconds
    """

    queryset_class = APIQuerySet

    def __init__(self, fetch_func: Callable, cache_timeout: int = 300):
        """Initialize with API fetch function.

        Args:
            fetch_func: Callable that returns list of data
            cache_timeout: Cache duration in seconds (default: 5 minutes)
        """
        super().__init__()
        self.fetch_func = fetch_func
        self.cache_timeout = cache_timeout

    def get_queryset(self):
        """Return queryset with data from API."""
        return self.queryset_class(
            model=self.model,
            fetch_func=self.fetch_func,
            cache_timeout=self.cache_timeout,
        )


class JSONQuerySetManager(VirtualManager):
    """Manager that loads data from JSON source.

    Args:
        json_source: Path to JSON file or JSON string
        json_path: Optional JSONPath to extract nested data
    """

    queryset_class = JSONQuerySet

    def __init__(self, json_source, json_path: Optional[str] = None):
        """Initialize with JSON source.

        Args:
            json_source: Path to file, JSON string, or dict
            json_path: Optional path to nested data (e.g., 'results.items')
        """
        super().__init__()
        self.json_source = json_source
        self.json_path = json_path

    def get_queryset(self):
        """Return queryset with data from JSON."""
        return self.queryset_class(
            model=self.model,
            json_source=self.json_source,
            json_path=self.json_path,
        )


class CachedQuerySetManager(VirtualManager):
    """Manager with caching support.

    Args:
        fetch_func: Callable that fetches data
        cache_key: Unique cache key
        cache_timeout: Cache duration in seconds
    """

    queryset_class = CachedQuerySet

    def __init__(
        self,
        fetch_func: Callable,
        cache_key: Optional[str] = None,
        cache_timeout: int = 3600,
    ):
        """Initialize with caching configuration.

        Args:
            fetch_func: Callable that returns data
            cache_key: Unique cache key (auto-generated if None)
            cache_timeout: Cache duration in seconds (default: 1 hour)
        """
        super().__init__()
        self.fetch_func = fetch_func
        self.cache_key = cache_key
        self.cache_timeout = cache_timeout

    def get_queryset(self):
        """Return queryset with caching."""
        return self.queryset_class(
            model=self.model,
            fetch_func=self.fetch_func,
            cache_key=self.cache_key,
            cache_timeout=self.cache_timeout,
        )

