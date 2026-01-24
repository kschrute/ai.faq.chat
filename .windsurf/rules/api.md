---
trigger: always
---

# API Development Best Practices

## API Design

- Use RESTful conventions for HTTP methods
- Return appropriate HTTP status codes
- Use consistent response formats
- Implement proper error handling

## Request Validation

- Validate all incoming request data
- Use schema validation (Pydantic, Zod)
- Sanitize user inputs
- Handle malformed requests gracefully

## Response Format

- Use consistent JSON structure
- Include metadata when needed (pagination, counts)
- Provide meaningful error messages
- Use proper HTTP headers

## Security

- Implement rate limiting
- Use HTTPS in production
- Validate authentication/authorization
- Sanitize outputs to prevent XSS

## Documentation

- Document API endpoints clearly
- Include request/response examples
- Document error responses
- Keep documentation up to date

## Performance

- Implement caching where appropriate
- Use efficient database queries
- Monitor API response times
- Implement pagination for large datasets

## Error Handling

- Use structured error responses
- Log errors appropriately
- Don't expose sensitive information
- Provide actionable error messages
