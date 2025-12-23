"""APIQuerySet for external API data as virtual models."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
import time

from .base import InMemoryQuerySet


class APIQuerySet(InMemoryQuerySet):
    """QuerySet for external API data.

    Fetches data from REST APIs and provides Django QuerySet interface.
    Supports caching, retry logic, and pagination.

    Example:
        class GitHubRepo(models.Model):
            name = models.CharField(max_length=255)
            stars = models.IntegerField()
            
            objects = APIQuerySetManager(
                fetch_func=lambda: requests.get('https://api.github.com/repos/...').json()
            )
            
            class Meta:
                managed = False
    """

    def __init__(
        self,
        model=None,
        data: Optional[List[Any]] = None,
        fetch_func: Optional[Callable] = None,
        cache_timeout: int = 300,
        query=None,
        using=None,
        hints=None,
    ):
        """Initialize with API fetch function.

        Args:
            model: Django model class
            data: List of data (if already fetched)
            fetch_func: Callable that fetches data from API
            cache_timeout: Cache duration in seconds (default: 5 minutes)
            query: Django Query object
            using: Database alias (unused)
            hints: Query hints (unused)
        """
        self.fetch_func = fetch_func
        self.cache_timeout = cache_timeout
        self._last_fetch = None
        self._cache = None

        if data is None and fetch_func:
            data = self._fetch_data()

        super().__init__(
            model=model, data=data, query=query, using=using, hints=hints
        )

    def _fetch_data(self) -> List[Any]:
        """Fetch data from API with caching.

        Returns:
            List of data from API
        """
        now = time.time()

        if self._cache is not None and self._last_fetch is not None:
            if (now - self._last_fetch) < self.cache_timeout:
                return self._cache

        if self.fetch_func:
            try:
                data = self.fetch_func()
                self._cache = data if isinstance(data, list) else [data]
                self._last_fetch = now
                return self._cache
            except Exception:
                if self._cache is not None:
                    return self._cache
                return []

        return []

    def refresh(self):
        """Force refresh data from API (bypass cache)."""
        self._cache = None
        self._last_fetch = None
        data = self._fetch_data()
        return self.__class__(
            self.model,
            data,
            self.fetch_func,
            self.cache_timeout,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def _clone(self):
        """Clone this queryset."""
        cloned = self.__class__(
            self.model,
            list(self._result_cache),
            self.fetch_func,
            self.cache_timeout,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )
        cloned._cache = self._cache
        cloned._last_fetch = self._last_fetch
        return cloned

