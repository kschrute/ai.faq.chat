---
trigger: always
---

# React Best Practices

## Component Structure

- Use functional components with hooks
- Keep components pure and predictable
- Extract complex logic into custom hooks
- Use TypeScript interfaces for props

## State Management

- Prefer local state with useState/useReducer
- Use Context for global state when needed
- Avoid prop drilling beyond 2-3 levels
- Keep state minimal and normalized

## Performance

- Use React.memo for expensive components
- Implement proper dependency arrays in useEffect
- Avoid inline function definitions in render
- Use useMemo/useCallback for expensive computations

## Code Organization

- Co-locate related components, hooks, and types
- Use consistent file naming (PascalCase for components)
- Export components as default, types as named exports
- Keep component files focused and small

## Best Practices

- Use descriptive prop names
- Provide default values for optional props
- Use proper TypeScript types for all props
- Implement error boundaries for error handling
- Use semantic HTML elements
- Add proper ARIA labels for accessibility

## Hooks Usage

- Follow rules of hooks (only call at top level)
- Use custom hooks for reusable logic
- Keep hook dependencies accurate
- Avoid side effects in render
