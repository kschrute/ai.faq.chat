---
trigger: always
---

# Git Best Practices

## Commit Messages

- Use conventional commit format (type: description)
- Keep messages under 50 characters for subject
- Use imperative mood ("Add feature" not "Added feature")
- Include detailed body when necessary

## Branch Strategy

- Use descriptive branch names (feature/description, fix/issue)
- Keep branches focused on single features/fixes
- Regularly sync with main branch
- Delete merged branches

## Code Review

- Review all changes before merging
- Use pull requests for all changes
- Ensure tests pass and coverage is maintained
- Review for security vulnerabilities

## .gitignore

- Never commit sensitive files (.env, secrets)
- Ignore build artifacts and dependencies
- Ignore IDE-specific files
- Keep .gitignore up to date

## Workflow

- Commit small, logical changes
- Use meaningful commit messages
- Test before pushing
- Resolve merge conflicts properly

## Best Practices

- Never force push to shared branches
- Use git hooks for pre-commit checks
- Keep commit history clean
- Tag releases appropriately
