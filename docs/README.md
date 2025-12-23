## Assistant Guidelines

This file provides general guidelines for the AI assistant working on this project.

For detailed information, refer to:
- `AI.md` - Condensed reference guide for AI assistants (start here)
- `purpose.md` - Project purpose and goals
- `structure.md` - Project structure and module organization
- `development.md` - Development guidelines and best practices

### Quick Reference

- Always use `./service.py dev <command>` or `python service.py dev <command>` for project tooling
- Always use `./service.py quality <command>` or `python service.py quality <command>` for quality checks
- Always use `./service.py django <command>` or `python service.py django <command>` for Django commands
- Maintain clean module organization and separation of concerns
- Default to English for all code artifacts (comments, docstrings, logging, error strings, documentation snippets, etc.)
- Follow Python best practices and quality standards
- Keep dependencies minimal and prefer standard library
- Ensure all public APIs have type hints and docstrings
- Write tests for new functionality
- Source code in `src/` directory

### Django VirtualQuerySet-Specific Guidelines

- **QuerySet development**: All QuerySets must inherit from `InMemoryQuerySet` or another QuerySet class
- **Manager development**: Managers should inherit from `VirtualManager` or a specialized manager
- **Model development**: Virtual models must inherit from `VirtualModel` or `ReadOnlyVirtualModel` and have `managed = False` in Meta
- **Django compatibility**: QuerySets must be compatible with Django's QuerySet interface
- **Data sources**: Support loading data from Django settings, external APIs, JSON files, or in-memory data

### QuerySet Implementation Checklist

When creating a new QuerySet:
- [ ] Inherit from `InMemoryQuerySet` or another QuerySet class
- [ ] Implement data loading logic
- [ ] Support Django QuerySet methods (filter, exclude, order_by, etc.)
- [ ] Support lazy evaluation where possible
- [ ] Add tests for the QuerySet

### Manager Implementation Checklist

When creating a new Manager:
- [ ] Inherit from `VirtualManager` or a specialized manager
- [ ] Override `get_data()` to provide data source
- [ ] Set `queryset_class` to specify which QuerySet to use
- [ ] Add tests for the Manager

### Model Implementation Checklist

When creating a new Virtual Model:
- [ ] Inherit from `VirtualModel` or `ReadOnlyVirtualModel`
- [ ] Set `managed = False` in Meta
- [ ] Set `abstract = True` if it's a base model
- [ ] Define appropriate manager (e.g., `ConfigQuerySetManager`, `APIQuerySetManager`)
- [ ] Override `save()` and `delete()` if custom persistence logic is needed
- [ ] Add tests for the model
