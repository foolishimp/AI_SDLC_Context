# Acme Corporation Security Policy
**Version**: 2.1
**Last Updated**: 2024-Q4
**Status**: Mandatory

## Purpose
This policy establishes security requirements for all software development at Acme Corporation.

## Scope
All employees, contractors, and third-party developers working on Acme systems.

## Requirements

### 1. Authentication & Authorization
- All systems MUST use corporate SSO
- Multi-factor authentication (MFA) REQUIRED
- Session timeout: 30 minutes maximum
- Role-based access control (RBAC) enforced

### 2. Secrets Management
- NO hardcoded credentials
- Use HashiCorp Vault for secrets
- Rotate keys every 90 days
- Never commit secrets to version control

### 3. Code Security
- Security scanning before merge
- SAST (Static Application Security Testing) required
- DAST (Dynamic Application Security Testing) for production
- Dependency vulnerability scanning

### 4. Data Protection
- Encrypt data at rest (AES-256)
- Encrypt data in transit (TLS 1.3)
- Classify all data: Public, Internal, Confidential, Restricted
- PII must be encrypted and access-logged

### 5. Incident Response
- Report security incidents within 1 hour
- Follow incident response playbook
- Conduct post-incident review
- Update security measures based on learnings

## Compliance
Failure to comply may result in:
- Access revocation
- Disciplinary action
- Legal consequences (for severe violations)

## Exceptions
Security exceptions require written approval from CISO.

---
*For questions, contact security@acme.com*
