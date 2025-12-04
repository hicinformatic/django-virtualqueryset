## Assistant Guidelines

### Project Purpose

**django-virtualqueryset** is a Django library for creating QuerySet-like objects that are not backed by a database. It provides:
- In-memory QuerySet implementation with Django ORM-like API
- Support for filtering, ordering, slicing, and aggregation on arbitrary data sources
- Integration with Django admin for non-database models
- Compatibility with Django forms, serializers, and views
- Virtual models that behave like regular Django models without database tables

This is useful for:
- Displaying data from external APIs in Django admin
- Creating virtual models for configuration or computed data
- Combining data from multiple sources with QuerySet interface
- Read-only models that don't need database persistence

### Development Guidelines

- Always execute project tooling through `python dev.py <command>`.
- Default to English for comments, docstrings, and translations.
- Keep comments minimal and only when they clarify non-obvious logic.
- Avoid reiterating what the code already states clearly.
- Add comments only when they resolve likely ambiguity or uncertainty.
- **QuerySet API**: Implement as much of the Django QuerySet API as possible:
  - Filtering: `filter()`, `exclude()`, `get()`
  - Ordering: `order_by()`, `reverse()`
  - Slicing: `[start:end]`, `first()`, `last()`
  - Aggregation: `count()`, `exists()`
  - Iteration: Support for loops and list conversion
- **Virtual Models**: Models using VirtualQuerySet should:
  - Not have database tables (no migrations)
  - Implement `objects` manager with VirtualQuerySet
  - Support Django admin integration
  - Be read-only by default (override `save()` and `delete()` if needed)
- **Data Sources**: Support arbitrary data sources:
  - Lists/iterables of dictionaries
  - External API responses
  - Computed data
  - Cached results
  - Multiple sources combined
- **Admin Integration**: Provide utilities for using virtual models in Django admin:
  - Custom model admin base class
  - List display configuration
  - Filtering and search support
  - Actions support (where applicable)
- **Performance**: Optimize for in-memory operations:
  - Lazy evaluation where possible
  - Efficient filtering and sorting
  - Memory-aware for large datasets
- **Testing**: Use pytest-django for all tests with mock data sources.

