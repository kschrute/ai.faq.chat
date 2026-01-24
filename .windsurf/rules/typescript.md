---
trigger: always
---

# TypeScript Best Practices

## Type Safety

- Every .ts / .tsx file must be type-safe
- Never use 'any' type unless truly unavoidable (and add TODO + explanatory comment)
- Prefer unknown over any when typing unknown data
- Enable all strict family options in tsconfig.json ("strict": true)
- Use as const for literal types when appropriate
- Implement proper null checks with optional chaining

## Best Practices

- Use interfaces for object shapes, types for unions/primitives
- Prefer explicit return types for public functions
- Use readonly for immutable properties
- Implement proper error handling with typed errors

## Code Organization

- Group related types in dedicated files or at top of files
- Use consistent naming conventions (PascalCase for types)
- Export types separately from implementations
- Use barrel exports for clean imports

## Advanced TypeScript

- Use utility types (Pick, Omit, Partial) effectively
- Implement proper generic constraints
- Use conditional types for complex type logic
- Leverage type guards for runtime type checking

## React + TypeScript

- Use proper typing for props with interfaces
- Type hooks return values explicitly
- Use forwardRef with proper typing
- Implement proper event handler types
- Use FC type with generic props for components
- Type children prop explicitly (React.ReactNode)
- Use useCallback/useMemo with proper dependency typing

## Performance

- Avoid excessive type computations
- Use type assertions sparingly
- Keep type definitions simple and readable
- Use const assertions for immutable values

## Error Handling

- Use discriminated unions for error types
- Implement proper error boundaries in React
- Type catch blocks with unknown and type guards
- Use Result/Either patterns for error-prone operations

## Configuration

- Enable strict: true in tsconfig.json
- Use noImplicitAny: true
- Enable strictNullChecks: true
- Set noImplicitReturns: true
- Use noUnusedLocals and noUnusedParameters

## Tooling Integration

- Configure Biome for TypeScript formatting
- Use TypeScript ESLint rules for additional checks
- Enable path mapping for clean imports
- Set up proper build targets in tsconfig
