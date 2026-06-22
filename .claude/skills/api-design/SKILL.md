---
name: api-design
displayName: REST API Design Best Practices
description: Expert knowledge for designing clean, scalable, and maintainable REST APIs
category: skill
tags: [api, rest, http, design, architecture]
dependencies: []
version: 1.0.0
---

# REST API Design Best Practices

This skill provides expert guidance for designing REST APIs that are intuitive, scalable, and maintainable.

## URL Design Principles

### Resource-Based URLs
```
✅ Good:
GET    /api/v1/workflows
GET    /api/v1/workflows/123
POST   /api/v1/workflows
PUT    /api/v1/workflows/123
DELETE /api/v1/workflows/123

❌ Bad:
GET    /api/v1/getWorkflows
POST   /api/v1/createWorkflow
POST   /api/v1/deleteWorkflow
```

### Nested Resources
```
✅ Good:
GET /api/v1/workflows/123/sessions
GET /api/v1/workflows/123/sessions/456

⚠️ Avoid deep nesting (max 2 levels):
❌ /api/v1/workflows/123/sessions/456/events/789/logs
✅ /api/v1/events/789/logs?session_id=456
```

### Query Parameters
```
# Filtering
GET /api/v1/workflows?status=active&tag=research

# Sorting
GET /api/v1/workflows?sort=created_at:desc

# Pagination
GET /api/v1/workflows?page=2&limit=20

# Field selection
GET /api/v1/workflows?fields=id,name,status
```

## HTTP Methods

### Standard CRUD Operations
| Method | Action | Request Body | Response | Idempotent |
|--------|--------|--------------|----------|------------|
| GET | Read | No | Resource | Yes |
| POST | Create | Yes | New resource | No |
| PUT | Replace | Yes | Updated resource | Yes |
| PATCH | Update | Yes | Updated resource | No |
| DELETE | Delete | No | 204 No Content | Yes |

### Idempotency
```
# Idempotent: Multiple identical requests = same result
PUT /api/v1/workflows/123
DELETE /api/v1/workflows/123

# Not idempotent: Multiple requests = different results
POST /api/v1/workflows (creates multiple resources)
```

## HTTP Status Codes

### Success Codes (2xx)
- **200 OK**: Standard success response with body
- **201 Created**: Resource created successfully
  - Include `Location` header with new resource URL
- **204 No Content**: Success with no response body (DELETE)
- **206 Partial Content**: Partial GET (e.g., pagination)

### Client Error Codes (4xx)
- **400 Bad Request**: Invalid syntax or validation error
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource conflict (e.g., duplicate name)
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded

### Server Error Codes (5xx)
- **500 Internal Server Error**: Generic server error
- **502 Bad Gateway**: Upstream service error
- **503 Service Unavailable**: Temporary downtime
- **504 Gateway Timeout**: Upstream timeout

## Response Formats

### Success Response
```json
{
  "id": "wf-123",
  "name": "Deep Research",
  "status": "active",
  "created_at": "2025-01-19T10:30:00Z",
  "updated_at": "2025-01-19T15:45:00Z"
}
```

### Error Response (Standard)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Workflow name is required",
    "details": [
      {
        "field": "name",
        "message": "Must not be empty",
        "value": ""
      }
    ],
    "request_id": "req-abc123"
  }
}
```

### Pagination Response
```json
{
  "data": [
    { "id": "wf-1", "name": "Workflow 1" },
    { "id": "wf-2", "name": "Workflow 2" }
  ],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 156,
    "total_pages": 8,
    "has_more": true
  },
  "links": {
    "self": "/api/v1/workflows?page=2&limit=20",
    "first": "/api/v1/workflows?page=1&limit=20",
    "prev": "/api/v1/workflows?page=1&limit=20",
    "next": "/api/v1/workflows?page=3&limit=20",
    "last": "/api/v1/workflows?page=8&limit=20"
  }
}
```

## Versioning

### URL Versioning (Recommended)
```
https://api.example.com/v1/workflows
https://api.example.com/v2/workflows
```

### Header Versioning
```
GET /api/workflows
Accept: application/vnd.superagent.v1+json
```

### When to Bump Version
- ✅ Breaking changes (remove fields, change types)
- ✅ Change in authentication method
- ❌ Adding optional fields (backward compatible)
- ❌ Bug fixes

## Authentication & Security

### API Keys (Simple)
```
Authorization: Bearer sa_live_abc123def456
```

### JWT Tokens (Stateless)
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### OAuth 2.0 (Third-party access)
```
Authorization: Bearer oauth2_token_here
```

### Security Headers
```
# CORS
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type

# Rate limiting
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642608000
```

## Rate Limiting

### Response Headers
```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642608000
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

### Rate Limit Strategies
1. **Per User**: 100 requests/minute per API key
2. **Per IP**: 1000 requests/hour per IP
3. **Per Endpoint**: Different limits for expensive operations
4. **Burst Allowance**: Allow short bursts above limit

## Caching

### ETags
```
# First request
GET /api/v1/workflows/123
ETag: "686897696a7c876b7e"
200 OK

# Subsequent request
GET /api/v1/workflows/123
If-None-Match: "686897696a7c876b7e"
304 Not Modified (no body)
```

### Cache Headers
```
Cache-Control: public, max-age=300
Cache-Control: private, no-cache
Cache-Control: no-store (sensitive data)
```

## Best Practices Checklist

### Design
- [ ] Use nouns for resources, not verbs
- [ ] Use plural resource names (`/workflows`, not `/workflow`)
- [ ] Nest resources logically (max 2 levels)
- [ ] Support filtering, sorting, pagination
- [ ] Version your API from day one

### Implementation
- [ ] Return correct HTTP status codes
- [ ] Provide helpful error messages
- [ ] Include request IDs for debugging
- [ ] Validate input thoroughly
- [ ] Handle edge cases gracefully

### Security
- [ ] Use HTTPS everywhere
- [ ] Implement rate limiting
- [ ] Validate API keys/tokens
- [ ] Sanitize inputs (prevent injection)
- [ ] Set proper CORS headers

### Performance
- [ ] Implement caching (ETags, Cache-Control)
- [ ] Paginate large responses
- [ ] Support field selection to reduce payload
- [ ] Use compression (gzip)
- [ ] Optimize database queries

### Documentation
- [ ] Provide OpenAPI/Swagger spec
- [ ] Include example requests/responses
- [ ] Document error codes
- [ ] Explain rate limits
- [ ] Provide SDKs for common languages

## Common Pitfalls

### 1. Not Using HTTP Status Codes Correctly
```
❌ Bad: Returning 200 OK with error in body
{
  "success": false,
  "error": "Not found"
}

✅ Good: Returning 404 Not Found
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Workflow not found"
  }
}
```

### 2. Inconsistent Naming
```
❌ Bad:
/api/workflows
/api/getAllSessions
/api/create_component

✅ Good:
/api/workflows
/api/sessions
/api/components
```

### 3. Exposing Internal IDs
```
❌ Bad: Auto-increment IDs
GET /api/workflows/1
GET /api/workflows/2

✅ Good: UUIDs or opaque IDs
GET /api/workflows/wf_3FnqB8Cz
GET /api/workflows/wf_7KmPx9Ty
```

### 4. Not Handling Partial Failures
```
POST /api/workflows/batch
[
  { "name": "Workflow 1" },  // ✅ Success
  { "name": "" },             // ❌ Invalid
  { "name": "Workflow 3" }   // ✅ Success
]

Response:
{
  "success": [
    { "index": 0, "id": "wf-1" },
    { "index": 2, "id": "wf-3" }
  ],
  "errors": [
    {
      "index": 1,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Name is required"
      }
    }
  ]
}
```

## Tools & Resources

### API Documentation
- Swagger UI: Interactive API documentation
- Postman: API testing and documentation
- Redoc: Clean API documentation generator

### Validation
- JSON Schema: Validate request/response structure
- OpenAPI Spec: Define API contract

### Testing
- Postman/Insomnia: Manual API testing
- Artillery/k6: Load testing
- Pact: Contract testing
