---
name: testing-patterns
displayName: Software Testing Patterns & Strategies
description: Comprehensive testing patterns, strategies, and best practices for reliable software
category: skill
tags: [testing, tdd, bdd, mocking, fixtures, coverage]
dependencies: []
version: 1.0.0
---

# Software Testing Patterns & Strategies

This skill provides expert knowledge for implementing comprehensive testing strategies across all layers of an application.

## Testing Pyramid

```
        ╱╲
       ╱  ╲
      ╱ E2E ╲      ← Few (5-10%)
     ╱──────╲
    ╱ Integr ╲     ← Some (20-30%)
   ╱──────────╲
  ╱   Unit     ╲   ← Many (60-70%)
 ╱──────────────╲
```

### Unit Tests (60-70%)
- Fast execution (<100ms each)
- Test individual functions in isolation
- Mock all external dependencies
- High coverage of edge cases

### Integration Tests (20-30%)
- Test component interactions
- Use real database (test DB)
- Test API endpoints end-to-end
- Verify data flows correctly

### E2E Tests (5-10%)
- Test critical user journeys
- Use real browser (Playwright/Cypress)
- Slowest but most realistic
- Focus on happy path + critical flows

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle

```
1. 🔴 RED: Write a failing test
2. 🟢 GREEN: Write minimal code to pass
3. 🔵 REFACTOR: Improve code without breaking tests
4. Repeat
```

### Example TDD Flow

```typescript
// 1. 🔴 RED: Write failing test
describe('Workflow', () => {
  test('validates required name field', () => {
    expect(() => new Workflow({ name: '' })).toThrow('Name is required')
  })
})

// Test fails (Workflow class doesn't exist yet)

// 2. 🟢 GREEN: Minimal implementation
class Workflow {
  constructor({ name }) {
    if (!name) throw new Error('Name is required')
    this.name = name
  }
}

// Test passes!

// 3. 🔵 REFACTOR: Improve code
class Workflow {
  constructor({ name, description = '' }) {
    this.validateName(name)
    this.name = name
    this.description = description
  }

  private validateName(name: string) {
    if (!name || name.trim() === '') {
      throw new Error('Name is required')
    }
  }
}

// Test still passes, code is cleaner
```

## Behavior-Driven Development (BDD)

### Given-When-Then Pattern

```typescript
describe('Workflow creation', () => {
  test('should create workflow with valid data', () => {
    // GIVEN: I have valid workflow data
    const validData = {
      name: 'Deep Research',
      description: 'AI research workflow',
      orchestration: { pattern: 'ceo-worker', model: 'claude-sonnet-4' }
    }

    // WHEN: I create a workflow
    const workflow = createWorkflow(validData)

    // THEN: The workflow should be created successfully
    expect(workflow.id).toBeDefined()
    expect(workflow.name).toBe('Deep Research')
    expect(workflow.status).toBe('pending')
  })
})
```

### Feature File (Cucumber-style)

```gherkin
Feature: Workflow Management
  As a user
  I want to create and manage workflows
  So that I can automate AI agent tasks

  Scenario: Create a workflow with valid data
    Given I have a valid workflow configuration
    When I submit the workflow
    Then the workflow should be created
    And the workflow should have status "pending"
    And I should receive the workflow ID

  Scenario: Cannot create workflow without name
    Given I have a workflow configuration without a name
    When I submit the workflow
    Then I should receive an error "Name is required"
    And no workflow should be created
```

## Mocking & Stubbing

### Mock External Dependencies

```typescript
import { vi } from 'vitest'

describe('SessionLauncher', () => {
  test('launches Claude process with correct arguments', async () => {
    // Mock child_process.spawn
    const mockSpawn = vi.fn().mockReturnValue({
      on: vi.fn(),
      stdout: { on: vi.fn() },
      stderr: { on: vi.fn() }
    })

    vi.mock('child_process', () => ({
      spawn: mockSpawn
    }))

    const launcher = new SessionLauncher()
    await launcher.launch('workflow-123')

    // Assert spawn was called with correct args
    expect(mockSpawn).toHaveBeenCalledWith('claude', [
      '--headless',
      '--config=.super_agent_monitor/workflows/workflow-123/.claude',
      expect.stringContaining('--session-id=')
    ])
  })
})
```

### Stub API Responses

```typescript
// Stub external API
global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: async () => ({
    id: 'msg-123',
    content: [{ text: 'AI response here' }]
  })
})

// Test code that uses fetch
const response = await callAnthropicAPI('Hello')
expect(response.id).toBe('msg-123')

// Verify fetch was called correctly
expect(global.fetch).toHaveBeenCalledWith(
  'https://api.anthropic.com/v1/messages',
  expect.objectContaining({
    method: 'POST',
    headers: expect.objectContaining({
      'x-api-key': expect.any(String)
    })
  })
)
```

### Spy on Methods

```typescript
const logger = {
  info: vi.fn(),
  error: vi.fn()
}

// Test code that logs
await processWorkflow('wf-123')

// Verify logging happened
expect(logger.info).toHaveBeenCalledWith('Processing workflow', { id: 'wf-123' })
expect(logger.error).not.toHaveBeenCalled()
```

## Test Fixtures & Factories

### Fixture Pattern
```typescript
// tests/fixtures/workflows.ts
export const fixtures = {
  validWorkflow: {
    name: 'Test Workflow',
    description: 'Test description',
    orchestration: {
      pattern: 'ceo-worker',
      model: 'claude-sonnet-4'
    },
    components: {
      agents: ['researcher-primary'],
      skills: ['web-search'],
      hooks: [],
      scripts: []
    }
  },

  minimalWorkflow: {
    name: 'Minimal',
    orchestration: {
      pattern: 'star',
      model: 'claude-haiku-3'
    }
  },

  invalidWorkflow: {
    name: '',  // Invalid: empty name
    orchestration: {
      pattern: 'invalid-pattern',
      model: 'unknown-model'
    }
  }
}

// Usage in tests
import { fixtures } from './fixtures/workflows'

test('creates workflow', async () => {
  const workflow = await createWorkflow(fixtures.validWorkflow)
  expect(workflow.id).toBeDefined()
})
```

### Factory Pattern
```typescript
// tests/factories/workflow.factory.ts
import { v4 as uuid } from 'uuid'

export class WorkflowFactory {
  static create(overrides = {}) {
    return {
      id: uuid(),
      name: 'Test Workflow',
      description: 'Auto-generated test workflow',
      status: 'pending',
      created_at: new Date().toISOString(),
      orchestration: {
        pattern: 'ceo-worker',
        model: 'claude-sonnet-4'
      },
      ...overrides  // Override defaults
    }
  }

  static createActive() {
    return this.create({ status: 'active' })
  }

  static createCompleted() {
    return this.create({
      status: 'completed',
      completed_at: new Date().toISOString()
    })
  }
}

// Usage
const workflow = WorkflowFactory.create({ name: 'Custom Name' })
const activeWorkflow = WorkflowFactory.createActive()
```

## Snapshot Testing

```typescript
import { expect, test } from 'vitest'

test('workflow renders correctly', () => {
  const workflow = {
    id: 'wf-123',
    name: 'Deep Research',
    status: 'active'
  }

  const rendered = renderWorkflow(workflow)

  // First run: Creates snapshot file
  // Subsequent runs: Compares to snapshot
  expect(rendered).toMatchSnapshot()
})

// Snapshot file (auto-generated):
// exports[`workflow renders correctly 1`] = `
// {
//   "id": "wf-123",
//   "name": "Deep Research",
//   "status": "active"
// }
// `
```

## Parameterized Tests

```typescript
// Test multiple inputs efficiently
describe.each([
  { input: 'hello', expected: 'HELLO' },
  { input: 'world', expected: 'WORLD' },
  { input: '', expected: '' },
  { input: '123', expected: '123' }
])('toUpperCase($input)', ({ input, expected }) => {
  test(`returns ${expected}`, () => {
    expect(toUpperCase(input)).toBe(expected)
  })
})

// Generates 4 tests automatically:
// ✓ toUpperCase(hello) returns HELLO
// ✓ toUpperCase(world) returns WORLD
// ✓ toUpperCase() returns
// ✓ toUpperCase(123) returns 123
```

## Property-Based Testing

```typescript
import fc from 'fast-check'

// Test with random inputs to find edge cases
test('workflow name validation', () => {
  fc.assert(
    fc.property(fc.string(), (name) => {
      if (name.trim() === '') {
        // Empty strings should throw
        expect(() => new Workflow({ name })).toThrow()
      } else {
        // Non-empty strings should succeed
        const workflow = new Workflow({ name })
        expect(workflow.name).toBe(name)
      }
    })
  )
})

// Runs 100 random test cases automatically
```

## Async Testing Patterns

### Testing Promises
```typescript
test('fetches workflow data', async () => {
  const workflow = await fetchWorkflow('wf-123')
  expect(workflow.name).toBe('Deep Research')
})
```

### Testing Callbacks
```typescript
test('callback fires after completion', (done) => {
  processWorkflow('wf-123', (err, result) => {
    expect(err).toBeNull()
    expect(result.status).toBe('completed')
    done()  // Signal test completion
  })
})
```

### Testing Event Emitters
```typescript
test('emits status change event', async () => {
  const workflow = new Workflow({ name: 'Test' })

  // Listen for event
  const eventPromise = new Promise((resolve) => {
    workflow.on('statusChange', resolve)
  })

  // Trigger status change
  workflow.setStatus('active')

  // Wait for event
  const event = await eventPromise
  expect(event.status).toBe('active')
})
```

## Database Testing

### Setup/Teardown
```typescript
import { Pool } from 'pg'

let pool: Pool

beforeAll(async () => {
  // Create test database connection
  pool = new Pool({
    connectionString: process.env.TEST_DATABASE_URL
  })

  // Run migrations
  await pool.query(readFileSync('./schema.sql', 'utf8'))
})

afterAll(async () => {
  // Close connections
  await pool.end()
})

beforeEach(async () => {
  // Clear tables before each test
  await pool.query('TRUNCATE workflows, sessions CASCADE')
})

test('saves workflow to database', async () => {
  const workflow = await createWorkflow({ name: 'Test' })

  const result = await pool.query('SELECT * FROM workflows WHERE id = $1', [workflow.id])
  expect(result.rows).toHaveLength(1)
  expect(result.rows[0].name).toBe('Test')
})
```

### Transaction Rollback Pattern
```typescript
let client

beforeEach(async () => {
  client = await pool.connect()
  await client.query('BEGIN')  // Start transaction
})

afterEach(async () => {
  await client.query('ROLLBACK')  // Rollback all changes
  client.release()
})

// Every test runs in isolation
```

## Code Coverage Goals

```
Statement coverage:  >80%   ████████░░
Branch coverage:     >75%   ███████░░░
Function coverage:   >90%   █████████░
Line coverage:       >80%   ████████░░
```

### Critical Coverage Targets
- **Authentication**: 100% (security-critical)
- **Payment logic**: 100% (data-critical)
- **Business logic**: 90% (core functionality)
- **UI components**: 70% (focus on logic, not styling)

### Running Coverage
```bash
# Generate coverage report
npm test -- --coverage

# Coverage output
-------------------|---------|----------|---------|---------|
File               | % Stmts | % Branch | % Funcs | % Lines |
-------------------|---------|----------|---------|---------|
workflow.ts        |   92.5  |   85.7   |   100   |   91.3  |
session-launcher.ts|   87.2  |   75.0   |   90.0  |   86.5  |
-------------------|---------|----------|---------|---------|
```

## Testing Best Practices Checklist

### Test Structure
- [ ] Use descriptive test names (what, when, expected)
- [ ] One assertion per test (when possible)
- [ ] AAA pattern (Arrange, Act, Assert)
- [ ] No logic in tests (no if/else, loops)
- [ ] Independent tests (no shared state)

### Test Coverage
- [ ] Happy path covered
- [ ] Error cases covered
- [ ] Boundary conditions tested
- [ ] Edge cases identified and tested
- [ ] Overall coverage >80%

### Mocking
- [ ] Mock external dependencies (APIs, databases)
- [ ] Mock current time (Date.now()) for consistency
- [ ] Mock file system operations
- [ ] Verify mock calls (toHaveBeenCalledWith)
- [ ] Reset mocks between tests

### Performance
- [ ] Unit tests run in <5 seconds
- [ ] Integration tests run in <30 seconds
- [ ] E2E tests run in <5 minutes
- [ ] Parallel test execution enabled
- [ ] No unnecessary setup/teardown

### Maintenance
- [ ] Tests fail when code breaks
- [ ] Tests don't fail randomly (flaky)
- [ ] Easy to understand test failures
- [ ] Tests serve as documentation
- [ ] Regularly review and refactor tests

## Anti-Patterns to Avoid

### ❌ Testing Implementation Details
```typescript
// ❌ Bad: Tests internal method
test('calls private method', () => {
  const workflow = new Workflow({ name: 'Test' })
  expect(workflow._internalValidate()).toBe(true)
})

// ✅ Good: Tests public behavior
test('creates valid workflow', () => {
  const workflow = new Workflow({ name: 'Test' })
  expect(workflow.name).toBe('Test')
})
```

### ❌ Tests That Depend on Each Other
```typescript
// ❌ Bad: Test order matters
let workflowId
test('creates workflow', async () => {
  const workflow = await createWorkflow({ name: 'Test' })
  workflowId = workflow.id  // ⚠️ Shared state
})

test('retrieves workflow', async () => {
  const workflow = await getWorkflow(workflowId)  // ⚠️ Depends on previous test
  expect(workflow.name).toBe('Test')
})

// ✅ Good: Independent tests
test('retrieves workflow', async () => {
  const created = await createWorkflow({ name: 'Test' })
  const retrieved = await getWorkflow(created.id)
  expect(retrieved.name).toBe('Test')
})
```

### ❌ Brittle Tests (Break on UI Changes)
```typescript
// ❌ Bad: Relies on exact HTML structure
expect(element.querySelector('div > span > button').textContent).toBe('Submit')

// ✅ Good: Uses semantic queries
expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument()
```

## Tools & Frameworks

### Test Runners
- **Vitest**: Fast, modern (Vite-based)
- **Jest**: Popular, mature ecosystem
- **Mocha**: Flexible, minimal

### Assertion Libraries
- **Vitest/Jest**: Built-in matchers
- **Chai**: BDD-style assertions

### Mocking
- **Vitest**: Built-in mocking
- **Sinon**: Comprehensive spies/stubs
- **MSW**: Mock Service Worker (API mocking)

### E2E Testing
- **Playwright**: Multi-browser, fast
- **Cypress**: Great DX, Chrome-only
- **Puppeteer**: Headless Chrome automation

### Coverage
- **c8**: Native V8 coverage
- **Istanbul**: Industry standard
