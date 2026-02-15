# Security Skill

> Loaded by: RC-001, QA-006, and all agents during security tasks | Version: 1.0

## OWASP Top 10 Checklist

1. **Injection** - Parameterized queries, input validation, output encoding
2. **Broken Auth** - Strong passwords, MFA, secure sessions
3. **Sensitive Data** - HTTPS, encryption at rest, PII handling
4. **XXE** - Disable XML external entities and DTD processing
5. **Broken Access Control** - RBAC, resource ownership, path traversal prevention
6. **Security Misconfiguration** - No defaults, no info leaks, minimal surface
7. **XSS** - Output encoding, CSP headers, sanitized DOM manipulation
8. **Insecure Deserialization** - Input validation, type checking
9. **Vulnerable Components** - Regular dependency audits, no known CVEs
10. **Insufficient Logging** - Security events logged (without sensitive data), alerting

## Security Headers
```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
```

## Absolute Rules
- NEVER hardcode secrets, API keys, or passwords
- NEVER trust client-side validation alone
- NEVER log sensitive data (passwords, tokens, PII)
- NEVER use eval() with user input
- NEVER disable HTTPS in production
