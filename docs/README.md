## Assistant Guidelines

This file provides general guidelines for the AI assistant working on this project.

For detailed information, refer to:
- `AI.md` - Condensed reference guide for AI assistants (start here)
- `purpose.md` - Project purpose and goals
- `structure.md` - Project structure and module organization
- `development.md` - Development guidelines and best practices

### Quick Reference

- Always use `./service.py dev <command>` or `python dev.py <command>` for project tooling
- Always use `./service.py quality <command>` or `python quality.py <command>` for quality checks
- Maintain clean module organization and separation of concerns
- Default to English for all code artifacts (comments, docstrings, logging, error strings, documentation snippets, etc.)
- Follow Python best practices and quality standards
- Keep dependencies minimal and prefer standard library
- Ensure all public APIs have type hints and docstrings
- Write tests for new functionality

### Virtual QuerySet-Specific Guidelines

- **Virtual models**: All models must inherit from `VirtualModel` and set `managed = False`
- **Managers**: Use `VirtualManager` for QuerySet-like operations on virtual data
- **QuerySet operations**: Implement filtering, ordering, and data retrieval for virtual QuerySets
- **Django integration**: Ensure compatibility with Django's ORM patterns and admin interface
- **Data sources**: Support various data sources (APIs, in-memory data, configuration)

### Virtual Model Implementation Checklist

When creating a new virtual model:
- [ ] Inherit from `VirtualModel`
- [ ] Set `managed = False` in Meta
- [ ] Use `VirtualManager` as the manager
- [ ] Implement data retrieval logic
- [ ] Support filtering and ordering operations
- [ ] Add tests for the model
