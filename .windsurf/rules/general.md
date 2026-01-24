---
trigger: always
---

# General Code Best Practices

## Code Quality

- Keep functions small and focused on a single responsibility
- Use descriptive variable and function names
- Add comments for complex business logic, not obvious code
- Prefer early returns over nested if statements
- Use meaningful error messages

## File Organization

- Group related functionality in the same directory
- Keep file names descriptive and consistent with their purpose
- Use index files for clean imports when appropriate
- Separate concerns (UI, logic, types, utilities)

## Dependencies

- Minimize external dependencies
- Prefer built-in browser APIs when possible
- Keep dependencies up to date for security
- Review new dependencies before adding

## Performance

- Avoid unnecessary re-renders in React components
- Use React.memo for expensive components
- Implement proper loading states
- Optimize bundle size with tree shaking

## Security

- Never commit sensitive data (API keys, passwords)
- Validate all user inputs
- Use HTTPS in production
- Implement proper authentication and authorization

## Testing

- Write unit tests for business logic
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests simple and focused
