# Windsurf Rules

This directory contains local Windsurf rules to enforce code best practices for the AI FAQ Chat project.

## Available Rules

- **`general.md`** - General code quality and organization practices
- **`typescript.md`** - TypeScript strict mode and type safety rules
- **`react.md`** - React component and hooks best practices
- **`python.md`** - Python code style and type hints
- **`api.md`** - API design and security practices
- **`testing.md`** - Testing strategies and organization
- **`git.md`** - Git workflow and commit message standards
- **`security.md`** - Security best practices and data protection
- **`performance.md`** - Performance optimization guidelines

## Usage

These rules are automatically enforced by Windsurf during development. Each rule file has the `trigger: always` directive, ensuring they apply to all relevant files in the codebase.

## Project-Specific Context

This project uses:

- **Frontend**: React + TypeScript with Vite
- **Backend**: Python with FastAPI
- **Linting**: Biome for frontend, ruff for Python
- **Testing**: Unit tests for critical components
- **Deployment**: Docker with Fly.io

The rules are tailored to this tech stack and project structure. All rules use `trigger: always` to ensure they apply during development.
