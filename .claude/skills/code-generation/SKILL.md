---
name: code-generation
displayName: Code Generation Skill
description: Patterns and best practices for generating high-quality code
category: skill
tags: [code, generation, patterns, best-practices]
dependencies: []
version: 1.0.0
---

# Code Generation Skill

Guide for generating clean, maintainable code across languages.

## Principles

1. **Clarity First**: Write code that reads like documentation
2. **Single Responsibility**: Each function does one thing well
3. **Error Handling**: Always handle edge cases
4. **Type Safety**: Use types/interfaces where available
5. **Testing**: Generate tests alongside implementation

## Patterns

### Function Generation
- Clear, descriptive names
- Parameter validation at entry
- Early returns for edge cases
- Consistent error handling

### Class Generation
- Small, focused classes
- Dependency injection
- Interface-based design
- Proper encapsulation

### API Generation
- RESTful conventions
- Proper HTTP methods
- Consistent response format
- Input validation

## Anti-Patterns to Avoid

- God classes/functions
- Magic numbers
- Deep nesting
- Implicit dependencies
