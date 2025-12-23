## Project Purpose

**Django VirtualQuerySet** is a Django library for creating QuerySet-like objects that are not backed by a database. It enables you to use Django's ORM patterns and admin interface with data from external sources.

### Core Functionality

The library enables you to:

1. **Create virtual models** that behave like Django models but don't have database tables:
   - Use Django admin interface with non-database data
   - Apply Django QuerySet methods (filter, exclude, order_by, etc.)
   - Support pagination, slicing, and iteration
   - Compatible with Django templates and views

2. **Load data from multiple sources**:
   - **Django settings**: Load configuration data as models
   - **External APIs**: Fetch data from REST APIs and use as QuerySets
   - **JSON files**: Load data from JSON files
   - **In-memory data**: Use Python lists/dicts directly
   - **Cached data**: Add caching to any data source

3. **QuerySet-like interface**:
   - All standard QuerySet methods (filter, exclude, get, first, count, etc.)
   - Chaining operations (filter().exclude().order_by())
   - Lazy evaluation
   - Slicing and iteration support

### Architecture

The library uses a QuerySet-based architecture:

- Each data source is implemented as a QuerySet class inheriting from `InMemoryQuerySet`
- Managers provide the interface between models and QuerySets
- Models inherit from `VirtualModel` or `ReadOnlyVirtualModel` (no database table)
- All QuerySet operations work on in-memory data structures

### Available QuerySets

- **`InMemoryQuerySet`**: Base QuerySet for in-memory data (lists, dicts)
- **`ConfigQuerySet`**: Loads data from Django settings
- **`APIQuerySet`**: Loads data from external APIs via HTTP requests
- **`JSONQuerySet`**: Loads data from JSON files
- **`CachedQuerySet`**: Adds caching layer to any QuerySet

### Available Managers

- **`VirtualManager`**: Base manager for virtual models
- **`ConfigQuerySetManager`**: Manager for Django settings data
- **`APIQuerySetManager`**: Manager for external API data
- **`JSONQuerySetManager`**: Manager for JSON file data
- **`CachedQuerySetManager`**: Manager with caching support

### Base Models

- **`VirtualModel`**: Base class for virtual models (no database table, raises on save/delete)
- **`ReadOnlyVirtualModel`**: Explicitly read-only virtual model

### Use Cases

- Display configuration/settings in Django admin
- Show data from external APIs in Django admin
- Create read-only models for reporting
- Integrate external data sources with Django views and templates
- Use Django QuerySet patterns with non-database data
- Build admin interfaces for data that doesn't live in the database
