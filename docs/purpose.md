## Project Purpose

**Django Virtual QuerySet** is a Django library for creating QuerySet-like objects that are not backed by a database.

### Core Functionality

The library enables you to:

1. **Create Virtual Models**:
   - Models that don't require database tables
   - Models backed by external APIs
   - Models using in-memory computed data
   - Configuration/settings as models
   - Read-only models without database tables

2. **Virtual QuerySet Operations**:
   - Filtering operations similar to Django QuerySets
   - Ordering operations
   - Data retrieval and iteration
   - Compatibility with Django ORM patterns

3. **Django Integration**:
   - Works seamlessly with Django admin
   - Compatible with Django's model system
   - Supports standard Django patterns

### Architecture

The library uses a manager-based architecture:

- `VirtualModel` provides the base model class
- `VirtualManager` handles QuerySet-like operations
- QuerySet utilities provide filtering, ordering, and data management
- Models can be used in Django admin without database tables

### Use Cases

- Data from external APIs displayed as Django models
- In-memory computed data represented as models
- Configuration/settings exposed as models
- Read-only models without database tables
- Migration path for existing tools that need virtual QuerySets
