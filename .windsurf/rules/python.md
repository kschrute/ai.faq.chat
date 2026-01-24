---
trigger: always
---

# Python Best Practices

## Code Style

- Follow PEP 8 style guidelines
- Use ruff for formatting and linting
- Keep lines under 88 characters (Black standard)
- Use meaningful variable and function names

## Type Hints

- Add type hints to all function signatures
- Use from __future__ import annotations for Python 3.7+
- Prefer specific types over generic ones
- Use typing.Optional for nullable values

## Error Handling

- Use specific exception types
- Handle exceptions at appropriate levels
- Include meaningful error messages
- Use finally blocks for cleanup

## Imports

- Group imports: standard library, third-party, local
- Use absolute imports over relative ones
- Avoid wildcard imports
- Keep import statements organized

## Code Organization

- Use modules and packages effectively
- Keep functions small and focused
- Use docstrings for public functions and classes
- Follow single responsibility principle

## Security

- Never hardcode secrets or credentials
- Validate all external inputs
- Use environment variables for configuration
- Follow secure coding practices

## Performance

- Use built-in functions and data structures
- Avoid unnecessary loops and computations
- Use generators for large datasets
- Profile code before optimizing
