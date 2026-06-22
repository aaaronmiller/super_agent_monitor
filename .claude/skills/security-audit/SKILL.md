---
name: security-audit
displayName: Security Audit & Best Practices
description: Comprehensive security audit checklist and vulnerability assessment techniques
category: skill
tags: [security, audit, vulnerabilities, owasp, pentest]
dependencies: []
version: 1.0.0
---

# Security Audit & Best Practices

This skill provides expert guidance for conducting security audits and implementing security best practices.

## OWASP Top 10 (2021)

### 1. Broken Access Control

**Vulnerability:**
```typescript
// ❌ Bad: No authorization check
app.get('/api/workflows/:id', async (req, res) => {
  const workflow = await db.query('SELECT * FROM workflows WHERE id = $1', [req.params.id])
  res.json(workflow)  // Anyone can access any workflow!
})
```

**Fix:**
```typescript
// ✅ Good: Check ownership
app.get('/api/workflows/:id', authenticateUser, async (req, res) => {
  const workflow = await db.query(
    'SELECT * FROM workflows WHERE id = $1 AND user_id = $2',
    [req.params.id, req.user.id]
  )
  if (!workflow) return res.status(404).json({ error: 'Not found' })
  res.json(workflow)
})
```

### 2. Cryptographic Failures

**Vulnerabilities:**
```typescript
// ❌ Bad: Storing passwords in plaintext
await db.query('INSERT INTO users (email, password) VALUES ($1, $2)',
  [email, password])

// ❌ Bad: Weak hashing
const hash = crypto.createHash('md5').update(password).digest('hex')

// ❌ Bad: Using HTTP for sensitive data
fetch('http://api.example.com/payment', { ... })
```

**Fixes:**
```typescript
// ✅ Good: Use bcrypt for passwords
import bcrypt from 'bcrypt'
const hashedPassword = await bcrypt.hash(password, 12)  // 12 rounds
await db.query('INSERT INTO users (email, password_hash) VALUES ($1, $2)',
  [email, hashedPassword])

// ✅ Good: Always use HTTPS
fetch('https://api.example.com/payment', { ... })

// ✅ Good: Encrypt sensitive data at rest
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto'

function encrypt(text: string, key: Buffer): string {
  const iv = randomBytes(16)
  const cipher = createCipheriv('aes-256-gcm', key, iv)
  const encrypted = Buffer.concat([cipher.update(text, 'utf8'), cipher.final()])
  const tag = cipher.getAuthTag()
  return Buffer.concat([iv, tag, encrypted]).toString('base64')
}
```

### 3. Injection (SQL, NoSQL, Command)

**SQL Injection:**
```typescript
// ❌ CRITICAL: SQL Injection vulnerability
app.get('/api/workflows', async (req, res) => {
  const query = `SELECT * FROM workflows WHERE name = '${req.query.name}'`
  const result = await db.query(query)
  // Attacker input: ' OR '1'='1' --
  // Query becomes: SELECT * FROM workflows WHERE name = '' OR '1'='1' --'
  res.json(result.rows)
})

// ✅ Good: Use parameterized queries
app.get('/api/workflows', async (req, res) => {
  const result = await db.query(
    'SELECT * FROM workflows WHERE name = $1',
    [req.query.name]
  )
  res.json(result.rows)
})
```

**Command Injection:**
```typescript
// ❌ CRITICAL: Command injection
const { exec } = require('child_process')
app.post('/api/convert', (req, res) => {
  exec(`convert ${req.body.filename} output.png`, (err, stdout) => {
    // Attacker input: "file.jpg; rm -rf /"
    res.send(stdout)
  })
})

// ✅ Good: Validate and sanitize input
import { spawn } from 'child_process'
app.post('/api/convert', (req, res) => {
  const filename = path.basename(req.body.filename)  // Remove path traversal
  if (!/^[a-zA-Z0-9._-]+$/.test(filename)) {
    return res.status(400).json({ error: 'Invalid filename' })
  }

  const convert = spawn('convert', [filename, 'output.png'])
  convert.on('close', (code) => {
    if (code === 0) res.json({ success: true })
    else res.status(500).json({ error: 'Conversion failed' })
  })
})
```

### 4. Insecure Design

**Example: Missing Rate Limiting**
```typescript
// ❌ Bad: No rate limiting on authentication
app.post('/api/login', async (req, res) => {
  const user = await db.query('SELECT * FROM users WHERE email = $1', [req.body.email])
  if (user && await bcrypt.compare(req.body.password, user.password_hash)) {
    res.json({ token: generateToken(user) })
  } else {
    res.status(401).json({ error: 'Invalid credentials' })
  }
  // Attacker can brute-force passwords!
})

// ✅ Good: Implement rate limiting
import rateLimit from 'express-rate-limit'

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // 5 attempts
  message: 'Too many login attempts, please try again later'
})

app.post('/api/login', loginLimiter, async (req, res) => {
  // ... authentication logic
})
```

### 5. Security Misconfiguration

**Checklist:**
```typescript
// ❌ Bad: Exposing stack traces in production
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack })  // Leaks internal paths!
})

// ✅ Good: Generic error messages in production
app.use((err, req, res, next) => {
  console.error(err)  // Log internally
  if (process.env.NODE_ENV === 'production') {
    res.status(500).json({ error: 'Internal server error' })
  } else {
    res.status(500).json({ error: err.message, stack: err.stack })
  }
})

// ❌ Bad: Using default credentials
const db = new Database({
  user: 'admin',
  password: 'admin123'
})

// ✅ Good: Use environment variables
const db = new Database({
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
})

// ❌ Bad: Unnecessary services enabled
// Leaving debug endpoints in production

// ✅ Good: Disable debug features in production
if (process.env.NODE_ENV !== 'production') {
  app.get('/debug', debugHandler)
}
```

### 6. Vulnerable and Outdated Components

**Audit Dependencies:**
```bash
# Check for known vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix breaking changes
npm audit fix --force

# Check outdated packages
npm outdated

# Update packages
npm update
```

**Dependabot Configuration (`.github/dependabot.yml`):**
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### 7. Identification and Authentication Failures

**Password Requirements:**
```typescript
// ✅ Strong password validation
function validatePassword(password: string): boolean {
  if (password.length < 12) return false  // Minimum 12 characters
  if (!/[a-z]/.test(password)) return false  // Lowercase letter
  if (!/[A-Z]/.test(password)) return false  // Uppercase letter
  if (!/[0-9]/.test(password)) return false  // Number
  if (!/[^a-zA-Z0-9]/.test(password)) return false  // Special character

  // Check against common passwords
  const commonPasswords = ['password123', 'qwerty123', ...]
  if (commonPasswords.includes(password.toLowerCase())) return false

  return true
}
```

**Session Management:**
```typescript
// ✅ Secure session configuration
import session from 'express-session'

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // Prevent XSS
    sameSite: 'strict',  // CSRF protection
    maxAge: 3600000      // 1 hour
  }
}))
```

**JWT Best Practices:**
```typescript
// ✅ Secure JWT implementation
import jwt from 'jsonwebtoken'

// Generate token
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '1h', algorithm: 'HS256' }
)

// Verify token
function authenticateToken(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) return res.status(401).json({ error: 'No token provided' })

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    req.user = decoded
    next()
  } catch (err) {
    res.status(403).json({ error: 'Invalid token' })
  }
}
```

### 8. Software and Data Integrity Failures

**Verify Dependencies:**
```bash
# Use package-lock.json to ensure consistent installs
npm ci  # Instead of npm install

# Verify package integrity
npm install --integrity
```

**Code Signing:**
```bash
# Sign git commits
git config --global user.signingkey <GPG-KEY-ID>
git config --global commit.gpgSign true
```

### 9. Security Logging and Monitoring Failures

**Audit Logging:**
```typescript
// ✅ Log security events
import winston from 'winston'

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'security.log' })
  ]
})

// Log authentication attempts
app.post('/api/login', async (req, res) => {
  const user = await authenticate(req.body.email, req.body.password)

  if (user) {
    logger.info('Login success', {
      userId: user.id,
      email: req.body.email,
      ip: req.ip,
      userAgent: req.headers['user-agent']
    })
  } else {
    logger.warn('Login failed', {
      email: req.body.email,
      ip: req.ip,
      userAgent: req.headers['user-agent']
    })
  }
})

// Log access control failures
function checkPermission(req, res, next) {
  if (!req.user.hasPermission(req.path)) {
    logger.warn('Access denied', {
      userId: req.user.id,
      path: req.path,
      method: req.method,
      ip: req.ip
    })
    return res.status(403).json({ error: 'Forbidden' })
  }
  next()
}
```

### 10. Server-Side Request Forgery (SSRF)

**Vulnerability:**
```typescript
// ❌ CRITICAL: SSRF vulnerability
app.post('/api/fetch-url', async (req, res) => {
  const response = await fetch(req.body.url)
  // Attacker input: http://localhost:6379/  (access internal Redis)
  // Attacker input: http://169.254.169.254/latest/meta-data/  (AWS metadata)
  res.send(await response.text())
})
```

**Fix:**
```typescript
// ✅ Good: Validate and restrict URLs
import { URL } from 'url'

const ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com']
const BLOCKED_IPS = ['127.0.0.1', '0.0.0.0', '169.254.169.254']

app.post('/api/fetch-url', async (req, res) => {
  try {
    const url = new URL(req.body.url)

    // Check protocol
    if (!['http:', 'https:'].includes(url.protocol)) {
      return res.status(400).json({ error: 'Invalid protocol' })
    }

    // Check domain whitelist
    if (!ALLOWED_DOMAINS.includes(url.hostname)) {
      return res.status(400).json({ error: 'Domain not allowed' })
    }

    // Prevent access to internal IPs
    const ip = await dns.promises.resolve(url.hostname)
    if (BLOCKED_IPS.some(blocked => ip.includes(blocked))) {
      return res.status(400).json({ error: 'IP not allowed' })
    }

    const response = await fetch(url.toString(), { timeout: 5000 })
    res.send(await response.text())
  } catch (err) {
    res.status(400).json({ error: 'Invalid URL' })
  }
})
```

## Security Headers

```typescript
import helmet from 'helmet'

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    }
  },
  hsts: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true
  }
}))

// Additional headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff')
  res.setHeader('X-Frame-Options', 'DENY')
  res.setHeader('X-XSS-Protection', '1; mode=block')
  res.setHeader('Referrer-Policy', 'no-referrer')
  next()
})
```

## CORS Configuration

```typescript
import cors from 'cors'

// ❌ Bad: Allow all origins
app.use(cors())

// ✅ Good: Restrict origins
app.use(cors({
  origin: ['https://app.example.com', 'https://admin.example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))
```

## Input Validation

```typescript
import { z } from 'zod'

// ✅ Schema validation
const CreateWorkflowSchema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
  orchestration: z.object({
    pattern: z.enum(['ceo-worker', 'star', 'round-robin']),
    model: z.string()
  })
})

app.post('/api/workflows', async (req, res) => {
  try {
    const data = CreateWorkflowSchema.parse(req.body)
    // data is now validated and typed
    const workflow = await createWorkflow(data)
    res.json(workflow)
  } catch (err) {
    res.status(400).json({ error: 'Validation failed', details: err.errors })
  }
})
```

## Security Audit Checklist

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt (12+ rounds)
- [ ] Rate limiting on authentication endpoints
- [ ] Multi-factor authentication (MFA) available
- [ ] Session timeout configured
- [ ] JWT tokens expire (1-24 hours)
- [ ] Authorization checks on every endpoint
- [ ] Principle of least privilege enforced

### Data Protection
- [ ] HTTPS enforced (no HTTP)
- [ ] Sensitive data encrypted at rest
- [ ] Database credentials in environment variables
- [ ] API keys not committed to git
- [ ] Secrets managed securely (e.g., Vault)

### Input Validation
- [ ] All user inputs validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output escaping)
- [ ] CSRF protection enabled
- [ ] File upload restrictions (type, size)

### Dependencies
- [ ] No known vulnerabilities (npm audit clean)
- [ ] Dependencies up to date
- [ ] Dependabot enabled
- [ ] Minimal dependencies (reduce attack surface)

### Logging & Monitoring
- [ ] Security events logged
- [ ] Failed login attempts tracked
- [ ] Access control failures logged
- [ ] Log retention policy defined
- [ ] Alerts configured for suspicious activity

### Infrastructure
- [ ] Firewall configured
- [ ] Unnecessary services disabled
- [ ] Security headers set (Helmet.js)
- [ ] CORS properly configured
- [ ] Database not exposed to internet
- [ ] Backups encrypted and tested

### Code Quality
- [ ] No hardcoded secrets
- [ ] Error messages don't leak sensitive info
- [ ] Debug mode disabled in production
- [ ] Code reviewed for security issues
- [ ] Static analysis tools used (e.g., Semgrep)
