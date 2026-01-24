---
trigger: always
---

# Testing Best Practices

## Test Organization

- Group tests by feature/module
- Use descriptive test names that explain what is being tested
- Arrange-Act-Assert pattern for test structure
- Keep tests independent and isolated

## Unit Tests

- Test public interfaces, not implementation details
- Mock external dependencies
- Test edge cases and error conditions
- Aim for high code coverage but focus on critical paths

## Integration Tests

- Test component interactions
- Test API endpoints with real data flow
- Use test databases/fixtures
- Test error scenarios

## Test Data

- Use realistic test data
- Avoid magic numbers and strings
- Create reusable test fixtures
- Clean up test data after tests

## Assertions

- Use specific assertion messages
- Test one thing per test
- Use appropriate matchers
- Verify both positive and negative cases

## Mocking

- Mock external services and APIs
- Use dependency injection for testability
- Verify mock interactions when important
- Avoid over-mocking

## Best Practices

- Write tests before fixing bugs (regression tests)
- Keep tests simple and readable
- Run tests automatically in CI/CD
- Review test coverage regularly
