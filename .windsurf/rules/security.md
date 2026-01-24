---
trigger: always
---

# Security Best Practices

## Data Protection

- Never hardcode secrets, API keys, or passwords
- Use environment variables for sensitive configuration
- Encrypt sensitive data at rest and in transit
- Implement proper access controls

## Input Validation

- Validate all user inputs on both client and server
- Sanitize data to prevent injection attacks
- Use parameterized queries for database operations
- Implement rate limiting to prevent abuse

## Authentication & Authorization

- Use strong authentication mechanisms
- Implement proper session management
- Follow principle of least privilege
- Regularly rotate secrets and credentials

## API Security

- Use HTTPS in production
- Implement CORS policies appropriately
- Add security headers (CSP, HSTS, etc.)
- Validate and sanitize API responses

## Dependencies

- Regularly update dependencies for security patches
- Use dependency scanning tools
- Review third-party code before inclusion
- Pin dependency versions in production

## Code Security

- Avoid eval() and similar dangerous functions
- Use secure coding practices
- Implement proper error handling without information leakage
- Regular security reviews and audits

## Monitoring

- Log security events appropriately
- Monitor for suspicious activity
- Implement intrusion detection
- Have incident response procedures
