# Authentication Implementation Guide

## Overview

This document describes the authentication system for the AI Code Assistant backend API. We use JWT-based authentication with OAuth 2.0 for third-party integrations.

## Authentication Flow

### 1. User Registration
```
User -> POST /auth/register
  {
    "email": "user@example.com",
    "password": "secure_password",
    "name": "John Doe"
  }

Response: 201 Created
  {
    "user_id": "uuid",
    "message": "Verification email sent"
  }
```

### 2. Email Verification
- User receives email with verification token
- Click link: `GET /auth/verify?token={token}`
- Backend validates token and activates account

### 3. Login
```
User -> POST /auth/login
  {
    "email": "user@example.com",
    "password": "secure_password"
  }

Response: 200 OK
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600
  }
```

### 4. Token Refresh
```
User -> POST /auth/refresh
  {
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }

Response: 200 OK
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 3600
  }
```

## JWT Token Structure

### Access Token Payload
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "exp": 1700000000,
  "iat": 1699996400
}
```

### Refresh Token Payload
```json
{
  "sub": "user_id",
  "token_id": "refresh_token_uuid",
  "exp": 1702588400,
  "iat": 1699996400
}
```

## Security Considerations

### Password Storage
- Passwords hashed using bcrypt with cost factor 12
- Never store plaintext passwords
- Minimum password length: 12 characters
- Require mix of uppercase, lowercase, numbers, special chars

### Token Security
- Access tokens expire after 1 hour
- Refresh tokens expire after 30 days
- Refresh tokens stored in database for revocation
- Tokens signed with HS256 using secret from environment variable

### Rate Limiting
- Login attempts: 5 per 15 minutes per IP
- Registration: 3 per hour per IP
- Token refresh: 10 per hour per user

## OAuth 2.0 Integration

### Supported Providers
- GitHub
- Google
- Microsoft

### OAuth Flow
```
1. User clicks "Login with GitHub"
2. Redirect to GitHub OAuth page
3. User approves access
4. GitHub redirects back with authorization code
5. Backend exchanges code for access token
6. Fetch user info from GitHub API
7. Create or link account
8. Issue JWT tokens
```

### OAuth Endpoints
- `GET /auth/oauth/{provider}` - Initiate OAuth flow
- `GET /auth/oauth/{provider}/callback` - Handle OAuth callback

## API Protection

### Middleware
All protected endpoints require valid JWT in Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Error Responses
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Valid token but insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded

## Database Schema

### users table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  name VARCHAR(255),
  is_verified BOOLEAN DEFAULT FALSE,
  role VARCHAR(50) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### refresh_tokens table
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### oauth_accounts table
```sql
CREATE TABLE oauth_accounts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  provider VARCHAR(50) NOT NULL,
  provider_user_id VARCHAR(255) NOT NULL,
  access_token TEXT,
  refresh_token TEXT,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(provider, provider_user_id)
);
```

## Implementation Checklist

- [ ] Set up bcrypt password hashing
- [ ] Generate JWT secret and store in environment
- [ ] Implement registration endpoint with email validation
- [ ] Set up email service for verification
- [ ] Implement login endpoint with rate limiting
- [ ] Create JWT token generation utility
- [ ] Implement token refresh logic
- [ ] Add authentication middleware
- [ ] Set up OAuth providers (GitHub, Google, Microsoft)
- [ ] Implement OAuth callback handling
- [ ] Create database migration scripts
- [ ] Write unit tests for auth logic
- [ ] Add integration tests for auth flow
- [ ] Document API in OpenAPI/Swagger

## Testing

### Manual Testing
Use Postman collection: `auth-endpoints.postman.json`

### Automated Tests
```bash
pytest tests/test_auth.py -v
```

### Security Testing
- Run OWASP ZAP scan
- Test rate limiting
- Verify token expiration
- Attempt SQL injection on login
- Test password strength requirements

---

**Related Project**: #ai-code-assistant
