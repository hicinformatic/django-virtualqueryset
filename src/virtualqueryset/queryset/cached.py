"""CachedQuerySet with caching support."""

from __future__ import annotations

from typing import Any, Callable, List, Optional
import hashlib
import pickle
import time

from .base import InMemoryQuerySet


class CachedQuerySet(InMemoryQuerySet):
    """QuerySet with caching support.

    Wraps any data source with automatic caching to reduce expensive operations.
    Supports both in-memory and external cache backends.

    Example:
        class ExpensiveData(models.Model):
            name = models.CharField(max_length=255)
            
            objects = CachedQuerySetManager(
                fetch_func=expensive_api_call,
                cache_key='expensive_data',
                cache_timeout=3600
            )
            
            class Meta:
                managed = False
    """

    def __init__(
        self,
        model=None,
        data: Optional[List[Any]] = None,
        fetch_func: Optional[Callable] = None,
        cache_key: Optional[str] = None,
        cache_timeout: int = 3600,
        cache_backend=None,
        query=None,
        using=None,
        hints=None,
    ):
        """Initialize with caching configuration.

        Args:
            model: Django model class
            data: List of data (if already loaded)
            fetch_func: Callable that fetches data
            cache_key: Unique key for caching
            cache_timeout: Cache duration in seconds (default: 1 hour)
            cache_backend: Django cache backend (default: in-memory dict)
            query: Django Query object
            using: Database alias (unused)
            hints: Query hints (unused)
        """
        self.fetch_func = fetch_func
        self.cache_key = cache_key or self._generate_cache_key()
        self.cache_timeout = cache_timeout
        self.cache_backend = cache_backend or self._get_memory_cache()

        if data is None:
            data = self._get_cached_or_fetch()

        super().__init__(
            model=model, data=data, query=query, using=using, hints=hints
        )

    _memory_cache: Dict[str, tuple] = {}

    def _get_memory_cache(self):
        """Get in-memory cache dict."""
        return self._memory_cache

    def _generate_cache_key(self) -> str:
        """Generate cache key from model and fetch function."""
        if self.model:
            base = f"{self.model.__name__}"
        else:
            base = "cached_qs"

        if self.fetch_func:
            func_str = str(self.fetch_func)
            hash_val = hashlib.md5(func_str.encode()).hexdigest()[:8]
            return f"{base}_{hash_val}"

        return base

    def _get_cached_or_fetch(self) -> List[Any]:
        """Get data from cache or fetch if expired.

        Returns:
            List of cached or fresh data
        """
        now = time.time()

        if self.cache_key in self.cache_backend:
            cached_data, timestamp = self.cache_backend[self.cache_key]
            if (now - timestamp) < self.cache_timeout:
                return cached_data

        if self.fetch_func:
            try:
                data = self.fetch_func()
                data_list = data if isinstance(data, list) else [data]
                self.cache_backend[self.cache_key] = (data_list, now)
                return data_list
            except Exception:
                if self.cache_key in self.cache_backend:
                    cached_data, _ = self.cache_backend[self.cache_key]
                    return cached_data
                return []

        return []

    def invalidate_cache(self):
        """Clear cache for this queryset."""
        if self.cache_key in self.cache_backend:
            del self.cache_backend[self.cache_key]

    def refresh(self):
        """Force refresh data (bypass cache)."""
        self.invalidate_cache()
        data = self._get_cached_or_fetch()
        return self.__class__(
            self.model,
            data,
            self.fetch_func,
            self.cache_key,
            self.cache_timeout,
            self.cache_backend,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

    def _clone(self):
        """Clone this queryset."""
        return self.__class__(
            self.model,
            list(self._result_cache),
            self.fetch_func,
            self.cache_key,
            self.cache_timeout,
            self.cache_backend,
            self.query.clone(),
            using=self._db,
            hints=self._hints,
        )

